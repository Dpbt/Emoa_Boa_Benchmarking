
/*******************************************
 * Author: Zhongqiang Richard Ren. 
 * All Rights Reserved. 
 *******************************************/


#ifndef ZHONGQIANGREN_BASIC_SEARCH_BOALEX_H_
#define ZHONGQIANGREN_BASIC_SEARCH_BOALEX_H_

#include "search.hpp"
#include "search_dijkstra.hpp"
#include "algorithm"

#include <unordered_map>
#include <unordered_set>
#include <set>

#define DEBUG_BOALEX 0

namespace rzq{
namespace search{

using namespace rzq::basic;

typedef std::vector<double> CostVec;
/**
 * @brief A search label, used by BOA*.
 */
struct Label {
  Label() {};
  Label(long id0, long v0, const CostVec& g0, const CostVec& f0) {
    id = id0; v = v0; g = g0; f = f0;
  };
  long id; // label's id, make it easy to look up.
  long v;
  CostVec g;
  CostVec f;
};

std::ostream& operator<<(std::ostream& os, Label& l) ;

/**
 * @brief result data structure.
 */
struct BOALEXResult {
  std::unordered_map< long, std::vector<long> > paths;
  std::unordered_map< long, CostVec > costs;
  long n_generated = 0;
  long n_expanded = 0;
  long n_domCheck = 0;
  double rt_initHeu = 0.0;
  double rt_search = 0.0;
  bool timeout = false;
  double num_nondom_labels_avg = -1;
  double num_nondom_labels_max = -1;
};

/**
 * @brief an interface, depends on the impl of BOA*, TOA*, etc.
 */
class Frontier_BOALEX : public CostVec {
public:
  Frontier_BOALEX();
  virtual ~Frontier_BOALEX();
  virtual bool Check(CostVec g) ; // check if l is dominated or not.
  virtual void Update(Label l) ; // update the frontier using l.
  std::vector<long> label_ids;
  //std::unordered_map<long, Label> labels; // for BiPulse usage only...
  std::vector<Label> labels; // for BOA-lex
  // std::mutex ; // for BiPulse usage only...

// protected:
  // project the 3d vector to 2d vector by removing the first component.
  virtual CostVec _p(CostVec v);

  //virtual void Filter(CostVec v) ;
  // virtual bool Check2(CostVec v) ;
  //virtual void _rebuildTree(std::unordered_set<long> *skip_node);
protected:
  //virtual Filter_boa(std::unordered_map<long,Label> &a);
  //virtual basic::AVLNode* _filter(basic::AVLNode* n, const CostVec& k, int* outFlag=NULL);
  //virtual  _filter(std::vector<>* n, const CostVec& k, std::unordered_set<long> *a = NULL);
  //virtual basic::AVLNode* _rebuildTreeMethod(std::vector<long> &tree_node_ids, long start, long end);
  //virtual void _verifyNonDom(std::vector<long>&);
  //virtual bool _check(std::vector<>* n,const CostVec& k) ; // new impl @2021-08-31
};

//////////////////////////////////////////////////////////////////////

/**
 * @brief an interface / base class, use its pointer
 */
class BOALEX {
public:
  BOALEX();
  virtual ~BOALEX();
  // virtual void SetMode(const std::string in) ;

  // set graph as pointer, note to leverage polymorphism here.
  virtual void SetGraphPtr(basic::PlannerGraph* g) ;

  // this vd must be the same as the vd in Search().
  virtual void InitHeu(long vd);
  
  // heuristic computation are included in each search call.
  virtual int Search(long vo, long vd, double time_limit) ;

  virtual BOALEXResult GetResult() const ;

  /**
   * @brief a new API for python wrapper. only for grid like world. 
   * Add to make it compatible with pybind11.
   */
  // virtual void SetGrid(basic::GridkConn& g) ;
protected:
  // return the heuristic vector from v to vd.
  virtual CostVec _Heuristic(long v) ;

  // this method needs to new frontiers, which depend on the specific #obj.
  virtual void _UpdateFrontier(Label l) ;

  virtual long _GenLabelId() ;

  virtual bool _FrontierCheck(Label l) ;
  
  virtual bool _SolutionCheck(Label l) ;

  virtual void _PostProcRes();

  virtual std::vector<long> _BuildPath(long lid) ;

  virtual void _InitFrontiers() ;

  basic::PlannerGraph* _graph;

  // std::unordered_map< long, Frontier > _alpha; // map a vertex id (v) to alpha(v).
  //std::vector< Frontier > _alpha; // map a vertex id (v) to alpha(v).
  std::vector< Frontier_BOALEX* > _alpha; // map a vertex id (v) to alpha(v).
  //std::vector< FrontierNaive> _alpha;

  long _label_id_gen = 0;
  long _vo = -1, _vd = -1;
  std::set< std::pair< CostVec, long> > _open;

  // std::unordered_map<long, Label> _label;
  std::vector<Label> _label; 

  // std::unordered_map<long, long> _parent;
  std::vector<long> _parent;

  size_t __vec_alloc_total = 0;
  size_t __vec_alloc_batch = 1024;
  size_t __vec_alloc_batch_max = 1024*4;

  BOALEXResult _res;
  std::vector<Dijkstra> _dijks;
  // std::string _mode = ""; // for some special usage

  std::vector< std::vector<CostVec> > _heu_p2p;

  // basic::GridkConn temp_g; // temp, to be removed.
};

/**
 * @brief Add new cost dimension into the graph for testing purposes.
 * add_deg_cost=true means adding degree cost.
 * add_len_cost=true means adding the path length cost, i.e., each edge has a unit cost.
 */
void GraphExpandCostDim(rzq::basic::SparseGraph* g, bool add_deg_cost, bool add_len_cost) ;

/**
 * @brief The entry point of BOA*.
 * g - a pointer of graph, which can be either of class GridkConn or Roadmap. Polymorphism is used.
 * vo,vd - start and goal nodes.
 * time_limit - the run time limit for search.
 * res - the output argument.
 */
int RunBOALEX(rzq::basic::PlannerGraph* g, long vo, long vd, double time_limit, rzq::search::BOALEXResult* res);

/**
 * @brief Save the BOA* result to a file.
 */
int SaveBOALEXResult(std::string fname, const search::BOALEXResult& res);


} // end namespace search
} // end namespace zr

#endif  // ZHONGQIANGREN_BASIC_SEARCH_DIJKSTRA_H_
