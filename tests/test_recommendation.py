"""
Unit Tests for Recommendation Engine
Tests Graph-based PageRank algorithm
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.recommendation import RecommendationGraph


class TestRecommendationGraph(unittest.TestCase):
    """Test Recommendation Graph functionality"""

    def setUp(self):
        """Setup recommendation graph before each test"""
        self.graph = RecommendationGraph(damping_factor=0.85, iterations=20)

    def test_graph_initialization(self):
        """Test graph is properly initialized"""
        self.assertEqual(len(self.graph.users), 0)
        self.assertEqual(len(self.graph.products), 0)
        self.assertEqual(self.graph.damping_factor, 0.85)
        self.assertEqual(self.graph.iterations, 20)

    def test_add_interaction(self):
        """Test adding user-product interactions"""
        self.graph.add_interaction(1, 101, weight=1.0)
        self.graph.add_interaction(1, 102, weight=2.0)
        
        self.assertIn(1, self.graph.users)
        self.assertIn(101, self.graph.products)
        self.assertIn(102, self.graph.products)

    def test_interaction_weights(self):
        """Test interaction weights are tracked"""
        self.graph.add_interaction(1, 101, weight=1.0)
        self.graph.add_interaction(1, 101, weight=2.0)  # Add again
        
        neighbors = self.graph.get_neighbors(1)
        self.assertEqual(neighbors[101], 3.0)  # 1.0 + 2.0

    def test_get_neighbors(self):
        """Test getting user's interacted products"""
        self.graph.add_interaction(1, 101, weight=1.0)
        self.graph.add_interaction(1, 102, weight=2.0)
        self.graph.add_interaction(1, 103, weight=1.5)
        
        neighbors = self.graph.get_neighbors(1)
        self.assertEqual(len(neighbors), 3)
        self.assertEqual(neighbors[101], 1.0)
        self.assertEqual(neighbors[102], 2.0)
        self.assertEqual(neighbors[103], 1.5)

    def test_get_user_product_count(self):
        """Test counting users and products"""
        self.graph.add_interaction(1, 101)
        self.graph.add_interaction(1, 102)
        self.graph.add_interaction(2, 101)
        self.graph.add_interaction(2, 103)
        
        user_count, product_count = self.graph.get_user_product_count()
        self.assertEqual(user_count, 2)
        self.assertEqual(product_count, 3)

    def test_personalized_pagerank_basic(self):
        """Test basic PageRank recommendations"""
        # User 1 interacts with products 101, 102
        self.graph.add_interaction(1, 101, weight=2.0)
        self.graph.add_interaction(1, 102, weight=1.0)
        
        # User 2 interacts with products 102, 103
        self.graph.add_interaction(2, 102, weight=2.0)
        self.graph.add_interaction(2, 103, weight=1.0)
        
        # Get recommendations for User 1
        recommendations = self.graph.personalized_pagerank(1, top_k=2)
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 2)
        
        # Each recommendation is (product_id, score)
        for prod_id, score in recommendations:
            self.assertIsInstance(prod_id, int)
            self.assertIsInstance(score, float)

    def test_pagerank_excludes_interacted(self):
        """Test recommendations exclude already interacted products"""
        self.graph.add_interaction(1, 101, weight=5.0)
        self.graph.add_interaction(1, 102, weight=3.0)
        self.graph.add_interaction(2, 102)
        self.graph.add_interaction(2, 103)
        self.graph.add_interaction(2, 104)
        
        recommendations = self.graph.personalized_pagerank(1, top_k=5)
        
        # Should not recommend products user already strongly interacted with
        recommended_ids = [pid for pid, score in recommendations]
        # 103 and 104 should be prioritized over 101 and 102
        self.assertIn(103, recommended_ids)
        self.assertIn(104, recommended_ids)

    def test_pagerank_nonexistent_user(self):
        """Test PageRank for user not in graph"""
        recommendations = self.graph.personalized_pagerank(999, top_k=5)
        self.assertEqual(recommendations, [])

    def test_get_similar_users(self):
        """Test finding similar users using Jaccard similarity"""
        # User 1 and 2 both view products 101, 102
        self.graph.add_interaction(1, 101)
        self.graph.add_interaction(1, 102)
        
        self.graph.add_interaction(2, 101)
        self.graph.add_interaction(2, 102)
        self.graph.add_interaction(2, 103)
        
        # User 3 views different products
        self.graph.add_interaction(3, 104)
        self.graph.add_interaction(3, 105)
        
        similar = self.graph.get_similar_users(1, top_k=2)
        
        self.assertIsInstance(similar, list)
        self.assertGreater(len(similar), 0)
        
        # User 2 should be most similar (2 out of 3 products match)
        most_similar_user, similarity = similar[0]
        self.assertEqual(most_similar_user, 2)
        self.assertGreater(similarity, 0)

    def test_get_graph_stats(self):
        """Test getting graph statistics"""
        self.graph.add_interaction(1, 101)
        self.graph.add_interaction(1, 102)
        self.graph.add_interaction(2, 102)
        self.graph.add_interaction(2, 103)
        
        stats = self.graph.get_graph_stats()
        
        self.assertEqual(stats['total_users'], 2)
        self.assertEqual(stats['total_products'], 3)
        self.assertEqual(stats['total_edges'], 4)
        self.assertEqual(stats['avg_interactions_per_user'], 2.0)
        self.assertGreater(stats['density'], 0)


class TestRecommendationEdgeCases(unittest.TestCase):
    """Test edge cases"""

    def test_empty_graph(self):
        """Test operations on empty graph"""
        graph = RecommendationGraph()
        
        self.assertEqual(graph.get_neighbors(1), {})
        self.assertEqual(graph.personalized_pagerank(1), [])
        self.assertEqual(graph.get_similar_users(1), [])

    def test_single_user(self):
        """Test with only one user"""
        graph = RecommendationGraph()
        graph.add_interaction(1, 101)
        graph.add_interaction(1, 102)
        
        similar = graph.get_similar_users(1)
        self.assertEqual(similar, [])  # No other users

    def test_different_damping_factors(self):
        """Test with different damping factors"""
        graph1 = RecommendationGraph(damping_factor=0.5)
        graph2 = RecommendationGraph(damping_factor=0.95)
        
        self.assertEqual(graph1.damping_factor, 0.5)
        self.assertEqual(graph2.damping_factor, 0.95)


def run_recommendation_tests():
    """Run all recommendation tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_recommendation_tests()
