## 图的基本概念

### 图的定义

图由一个顶点集和连接各顶点的边集组成。它可以用二元组G=(V,E)表示，其中V表示顶点集，E表示边集。如果边有方向，则称为有向图，有向图的边用<>表示。<u,v>表示从u到v的一条边。无向图的路径用(u,v)表示。

边有可能还有第三个属性，就是边的代价或权值。以<u,v,w>(u,v,w)表示

任意一结点到另一结点至多只有1条边，有向图允许两个方向各有一条，这称为稀疏图，如果允许结点之间有多条边存在，则称为密集图。

## 图的基本术语

领接

存在一条连接两个结点的边，则可以说两结点相互邻接

度

在无向图中，结点的度是与该结点关联的边数。在有向图中，度被分为出度与入度

子图

整个图的一个小部分

路径与路径长度

非加权的路径长度就是组成路径的边数，加权路径长度是指路径上所有边的权值之和。

简单路径

除了终点和起点可能一样其他结点都不一样。

连通图和连通分量

如果无向图的任意两个结点之间都是连通的，则称其为连通图。非连通图都可以分成几个极大的连通的部分

强连通图和强连通分量

一个有向图任意两点之间是连通的，则其为强连通图，每个极大的强连通子图称为强连通分量

完全图

两个结点之间都有边的无向图称为无向完全图。每两个结点都有来回两个方向的边，则称为有向完全图

## 图的储存

### 1.邻接矩阵法

有n个顶点，则用n*n的矩阵表示整个图的关系，有向图也能表示。

有如下规律：

1. 对于无向图：矩阵的第i行或者第i列的元素之和是第i个结点的度。
2. 对于有向图：矩阵的第i行元素之和是结点i的出度，第i列元素之和是结点i的入度

### 2.邻接表表示法

基本的模式累死与hash-table因为用一个数组来储存各个结点，在每个结点后面再加上一个链表，链表中存有，该结点与另连通的某个结点的下标，如果是有权图，则是应该



# 最小生成树

## 最小生成树

bfs和dfs一个连通图都可以得到一棵生成树

带权值的无向连通图通常称为网络。

加权无向连通图的众多生成树中权值和最小的生成树称为最小生成树。

生成最小生成树的两种算法：Kruskal算法和Prim算法

#### 1.Kruskal算法

从边的角度出发，最开始生成树中只有点集，之后开始选n-1条路，依次选择权值最小的边

边的权值最小可以用优先队列维护，是否称为回路可以用并查集来实现

#### 2.Prim算法

从顶点出发，简单的讲，就是加入一个点，更新一次状态，一个新点的加入意味着加入这个新点所有的度，以终点比较价值，进行更新开始结点和价值，然后把这个加入的点加入到一个数列中。