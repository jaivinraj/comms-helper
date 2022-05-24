import pandas as pd
from itertools import combinations
import numpy as np
from sklearn.preprocessing import minmax_scale
import os
import time
import math
import logging
import igraph as ig
from functools import partial

from comms_helper.logging_utils import log_with_prefix

logging_prefix = "comms_helper.analysis.network"

log_with_mod_prefix = partial(log_with_prefix, logging_prefix=logging_prefix)


def centrality(g=None, metric_name="betweenness", weights="n_links_inv"):
    if metric_name == "betweenness":
        return g.betweenness(weights=weights)
    elif metric_name == "degree":
        return g.degree()
    elif metric_name == "eigenvector":
        return g.eigenvector_centrality(weights=weights)
    elif metric_name == "closeness":
        return g.closeness(weights=weights)
    else:
        raise Exception("Metric name provided is invalid")


class MyGraph(ig.Graph):
    def __init__(self, *args, **kwargs):
        super(MyGraph, self).__init__(*args, **kwargs)
        self.namearr = np.array(self.vs["name"])

    def _get_all_centralities(
        self, g=None, metric_names=["betweenness", "degree", "eigenvector", "closeness"]
    ):
        """Store centralities for all metrics in dictionary
        
        Parameters
        ----------
        metric_names: list of strings
            Metrics to compute
        """
        # self.centralities_ents = {}
        self.metric_names = metric_names
        for metric_name in metric_names:
            self.vs[metric_name] = centrality(self, metric_name)

    def _get_info_table(self):
        """Get table of info including various centralities and 

        ToDo
        ----
        * Add communities
        """
        self.info_table = pd.DataFrame(
            {metric_name: self.vs[metric_name] for metric_name in self.metric_names}
        )
        self.info_table = self.info_table.join(
            pd.Series(self.vs["community"]).to_frame("community")
        )
        self.info_table = self.info_table.join(
            pd.Series(self.vs["name"]).to_frame("name")
        )

    def _get_communities(self):
        """Perform a Louvain partitioning algorithm on the entity 
        network
        """
        self.louvain_partition = self.community_multilevel(weights="n_links_inv")
        self.vs["community"] = self.louvain_partition.membership

    def get_metrics(
        self,
        with_communities=True,
        metric_names=["betweenness", "degree", "eigenvector", "closeness"],
    ):
        """Calculate metrics for graph and obtain arrays for plotting

        Parameters
        ----------
        with_communities: bool
            whether to compute communities
        metric_names: list of strings
            Metrics to compute
        """
        log_with_mod_prefix("Getting centralities...")
        self._get_all_centralities(metric_names=metric_names)
        log_with_mod_prefix("Got centralities")
        if with_communities:
            log_with_mod_prefix("Getting communities...")
            self._get_communities()
            log_with_mod_prefix("Got communities")
        log_with_mod_prefix("Getting entity info table...")
        self._get_info_table()
        log_with_mod_prefix("Got entity info table")

    def get_subgraphs(self):
        """Get a subgraph for each community in the network
        """
        self.subgraphs = {}
        df_name_community = pd.DataFrame(
            {"name": self.vs["name"], "community": self.vs["community"]}
        )
        comm_labels = df_name_community["community"].unique()
        for label in comm_labels:
            self.subgraphs[label] = self.subgraph(
                df_name_community[df_name_community["community"] == label][
                    "name"
                ].values
            )

    def get_info_table_edges(self):
        self.info_table_edges = pd.DataFrame(
            {
                "id": self.es.indices,
                "n_links": self.es["n_links"],
                "n_links_inv": self.es["n_links_inv"],
            }
        )

    def prune_nodes(
        self, prune_attr="degree", cutoff=10, update_info=True, inplace=False
    ):
        prune_bool = self.info_table[prune_attr].values >= cutoff
        g_pruned = self.subgraph(self.namearr[prune_bool])
        g_pruned.namearr = np.array(g_pruned.vs["name"])
        update_info_nodes = False
        update_info_edges = False

        if update_info == True:
            update_info_nodes = True
            update_info_edges = True
        elif update_info == "nodes":
            update_info_nodes = True
        elif update_info == "edges":
            update_info_edges = True
        if update_info_nodes:
            g_pruned.get_metrics()
        else:
            g_pruned.info_table = self.info_table[prune_bool]
        if update_info_edges:
            g_pruned.get_info_table_edges()
        else:
            raise NotImplementedError
        return g_pruned

    def prune_edges(
        self, prune_attr="n_links", cutoff=10, update_info=True, inplace=False
    ):
        g_pruned = self.copy()
        edges_to_delete = self.info_table_edges.loc[
            self.info_table_edges[prune_attr] < cutoff, "id"
        ].values
        g_pruned.delete_edges(edges_to_delete)
        update_info_nodes = False
        update_info_edges = False

        if update_info == True:
            update_info_nodes = True
            update_info_edges = True
        elif update_info == "nodes":
            update_info_nodes = True
        elif update_info == "edges":
            update_info_edges = True
        if update_info_nodes:
            g_pruned.get_metrics()
        else:
            g_pruned.info_table = self.info_table
        if update_info_edges:
            g_pruned.get_info_table_edges()
        else:
            g_pruned.info_table_edges = self.info_table_edges[
                ~self.info_table_edges["id"].isin(edges_to_delete)
            ]
        return g_pruned

    def delete_single_nodes(self, recompute_degree=True):
        if recompute_degree:
            self.vs["degree"] = centrality(self, "degree")
        to_delete = self.namearr[np.array(self.vs["degree"]) == 0]
        self.delete_vertices(to_delete)


def get_edgelist(g):
    return [e.tuple for e in g.es]