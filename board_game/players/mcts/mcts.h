#ifndef __MCTS_H__
#define __MCTS_H__

#include <memory>
#include <cmath>
#include <algorithm>
#include <iterator>
#include <utility>
#include <random>
#include <chrono>
#include <map>
#include <future>

#include "utils.h"

template <class State>
class Node {
public:
    using NodePtr = std::unique_ptr<Node>;

    Node(const State& state, int player_id, const typename State::Action& action, Node* parent) : m_player_id(player_id), m_action(action), m_N(0), m_W(0), m_Q(0), m_unexpanded_actions(state.get_legal_actions(get_next_player_id(player_id))), m_children{}, m_parent(parent) {}
    Node(const Node& node);
    Node(Node&& node);

    bool is_fully_expanded() const { return m_unexpanded_actions.empty(); }
    Node* add_child(const State& state, int player_id, const typename State::Action& action, Node* parent) {
        m_children.push_back(std::make_unique<Node>(state, player_id, action, parent));
        m_unexpanded_actions.erase(std::remove(std::begin(m_unexpanded_actions), std::end(m_unexpanded_actions), action), std::end(m_unexpanded_actions));
        return m_children.back().get();
    }
    int get_player_id() const { return m_player_id; }
    const typename State::Action& get_action() const { return m_action; }
    int get_N() { return m_N; }
    typename State::Actions& get_unexpanded_actions() { return m_unexpanded_actions; }
    std::vector<NodePtr>& get_children() { return m_children; }
    Node* get_parent() { return m_parent; }
    void set_parent(Node* parent) { m_parent = parent; }
    double get_uct_value() const { return get_uct_value_exploitation_factor() + get_uct_value_exploration_factor(); }
    double get_uct_value_exploitation_factor() const { return m_Q; }
    double get_uct_value_exploration_factor() const { return sqrt(2 * log(m_parent->m_N) / m_N); }
    Node* uct_select_children() const {
        return std::max_element(std::begin(m_children), std::end(m_children), [](const NodePtr& node1, const NodePtr& node2){ return node1->get_uct_value() < node2->get_uct_value(); })->get();
    };
    void update(int V) {
        ++m_N;
        m_W += V;
        m_Q = static_cast<double>(m_W) / static_cast<double>(m_N);
    }

private:
    int                      m_player_id;
    typename State::Action   m_action;
    int                      m_N;
    int                      m_W;
    double                   m_Q;

    typename State::Actions  m_unexpanded_actions;
    std::vector<NodePtr>     m_children;
    Node*                    m_parent;
};

template <class State>
Node<State>::Node(const Node& node) : m_player_id(node.m_player_id), m_action(node.m_action), m_N(node.m_N), m_W(node.m_W), m_Q(node.m_Q), m_unexpanded_actions(node.m_unexpanded_actions), m_children{}, m_parent(node.m_parent) {
    m_children.reserve(node.m_children.size());
    for (const NodePtr& child : node.m_children) {
        m_children.emplace_back(std::make_unique<Node>(*child));
        m_children.back()->m_parent = this;
    }
}

template <class State>
Node<State>::Node(Node&& node) : m_player_id(node.m_player_id), m_action(std::move(node.m_action)), m_N(node.m_N), m_W(node.m_W), m_Q(node.m_Q), m_unexpanded_actions(std::move(node.m_unexpanded_actions)), m_children{std::move(node.m_children)}, m_parent(node.m_parent) {
    for (const NodePtr& child : m_children) child->m_parent = this;
}

template <class State>
class MctsTree {
public:
    MctsTree(const State& root_state, int player_id, int sim_num) : m_sim_num(sim_num), m_root_node(std::make_unique<Node<State>>(root_state, get_next_player_id(player_id), typename State::Action{}, nullptr)), m_root_state(std::make_unique<State>(root_state)) {}

    typename State::Action get_action(const State& state, int player_id);
    typename State::Action get_action_smt(const State& state, int player_id);

private:
    int                            m_sim_num;
    typename Node<State>::NodePtr  m_root_node;
    std::unique_ptr<State>         m_root_state;
};

template <class State>
typename State::Action MctsTree<State>::get_action(const State& state, int player_id) {
    assert(m_root_state->to_compact_string()==state.to_compact_string());
    assert(m_root_node->get_player_id()!=player_id);

    std::default_random_engine random_generator(std::chrono::system_clock::now().time_since_epoch().count());

    for (int i = 0; i < m_sim_num; ++i) {
        Node<State>* node{m_root_node.get()};
        std::unique_ptr<State> state{std::make_unique<State>(*m_root_state)};

        while (!state->is_end() && node->is_fully_expanded()) {
            node = node->uct_select_children();
            state->do_action(node->get_player_id(), node->get_action());
        }

        if (!state->is_end()) {
            const typename State::Actions& actions = node->get_unexpanded_actions();
            std::uniform_int_distribution<int> distribution(0, actions.size()-1);
            int index = distribution(random_generator);
            typename State::Action action = actions[index];
            int next_player_id = get_next_player_id(node->get_player_id());
            state->do_action(next_player_id, action);
            node = node->add_child(*state, next_player_id, action, node);
        }

        player_id = node->get_player_id();
        while (!state->is_end()) {
            player_id = get_next_player_id(player_id);
            const typename State::Actions& actions = state->get_legal_actions(player_id);
            std::uniform_int_distribution<int> distribution(0, actions.size()-1);
            int index = distribution(random_generator);
            typename State::Action action = actions[index];
            state->do_action(player_id, action);
        }

        int result = state->get_result();
        int V = (result > 0) ? ((result == node->get_player_id()) ? 1 : -1) : 0;
        while (node) {
            node->update(V);
            V = -V;
            node = node->get_parent();
        }
    }

    std::vector<typename Node<State>::NodePtr>& children {m_root_node->get_children()};
    typename Node<State>::NodePtr& child = *std::max_element(std::begin(children), std::end(children), [](const typename Node<State>::NodePtr& node1, const typename Node<State>::NodePtr& node2){ return node1->get_N() < node2->get_N(); });
    m_root_node.reset(child.release());
    m_root_node->set_parent(nullptr);
    m_root_state->do_action(m_root_node->get_player_id(), m_root_node->get_action());

    return m_root_node->get_action();
}

template <class State>
std::map<typename State::Action, int> search(Node<State> root_node, const State& root_state, int sim_num) {
    std::default_random_engine random_generator(std::chrono::system_clock::now().time_since_epoch().count());

    for (int i = 0; i < sim_num; ++i) {
        Node<State>* node{&root_node};
        std::unique_ptr<State> state{std::make_unique<State>(root_state)};

        while (!state->is_end() && node->is_fully_expanded()) {
            node = node->uct_select_children();
            state->do_action(node->get_player_id(), node->get_action());
        }

        if (!state->is_end()) {
            const typename State::Actions& actions = node->get_unexpanded_actions();
            std::uniform_int_distribution<int> distribution(0, actions.size()-1);
            int index = distribution(random_generator);
            typename State::Action action = actions[index];
            int next_player_id = get_next_player_id(node->get_player_id());
            state->do_action(next_player_id, action);
            node = node->add_child(*state, next_player_id, action, node);
        }

        int player_id = node->get_player_id();
        while (!state->is_end()) {
            player_id = get_next_player_id(player_id);
            const typename State::Actions& actions = state->get_legal_actions(player_id);
            std::uniform_int_distribution<int> distribution(0, actions.size()-1);
            int index = distribution(random_generator);
            typename State::Action action = actions[index];
            state->do_action(player_id, action);
        }

        int result = state->get_result();
        int V = (result > 0) ? ((result == node->get_player_id()) ? 1 : -1) : 0;
        while (node) {
            node->update(V);
            V = -V;
            node = node->get_parent();
        }
    }

    std::map<typename State::Action, int> action_to_N;
    for (typename Node<State>::NodePtr& child : root_node.get_children()) {
        action_to_N.emplace(child->get_action(), child->get_N());
    }
    return action_to_N;
}

template <class State>
typename State::Action MctsTree<State>::get_action_smt(const State& state, int player_id) {
    assert(m_root_state->to_compact_string()==state.to_compact_string());
    assert(m_root_node->get_player_id()!=player_id);

    const int THREAD_NUM = 4;
    std::vector<std::future<std::map<typename State::Action, int>>> futures;
    for (int i = 0; i < THREAD_NUM-1; ++i) {
        futures.push_back(std::async(search<State>, *m_root_node, std::ref(*m_root_state), m_sim_num));
    }
    std::map<typename State::Action, int> action_to_N = search<State>(*m_root_node, std::ref(*m_root_state), m_sim_num);
    for (int i = 0; i < THREAD_NUM-1; ++i) {
        std::map<typename State::Action, int> action_to_N_tmp = futures[i].get();
        for (const auto& e : action_to_N_tmp) {
            action_to_N[e.first] += e.second;
        }
    }

    typename State::Action action = std::max_element(std::begin(action_to_N), std::end(action_to_N), [](const std::pair<typename State::Action, int>& e1, const std::pair<typename State::Action, int>& e2){ return e1.second < e2.second; })->first;
    return action;
    //std::vector<Node::NodePtr>& children {m_root_node->get_children()};
    //Node::NodePtr& child = *std::find_if(std::begin(children), std::end(children), [&action](const Node::NodePtr& e) { return e->get_action() == action; });
    //m_root_node.reset(child.release());
    //m_root_node->set_parent(nullptr);
    //m_root_state->do_action(m_root_node->get_player_id(), m_root_node->get_action());

    //return m_root_node->get_action();
}

#endif

