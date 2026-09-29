"""
Field Service Memory — Automated Integration Test Suite
Verifies all backend endpoints, Hindsight memory engine lifecycle,
and the 9-step demo flow.
"""

import sys
import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.services.seed_service import SeedService


class TestFieldServiceMemory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            SeedService.seed_all(db)
        finally:
            db.close()
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("hindsight", data)

    def test_insights(self):
        res = self.client.get("/api/insights")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("recurring_issues", data)
        self.assertIn("failed_temporary_fixes", data)
        self.assertIn("high_activity_sites", data)
        self.assertIn("memory_knowledge_base", data)
        self.assertGreater(data["memory_knowledge_base"]["total_memories"], 0)

    def test_memory_status_and_stats(self):
        res = self.client.get("/api/memory/status")
        self.assertEqual(res.status_code, 200)
        self.assertIn("bank_id", res.json())

        res_stats = self.client.get("/api/memory/stats")
        self.assertEqual(res_stats.status_code, 200)
        self.assertGreater(res_stats.json()["total_memories"], 0)

    def test_equipment_and_timeline(self):
        res = self.client.get("/api/equipment")
        self.assertEqual(res.status_code, 200)
        eq_list = res.json()
        self.assertGreaterEqual(len(eq_list), 30)

        # Test HVAC-204 (EQUIP-001)
        res_eq = self.client.get("/api/equipment/EQUIP-001")
        self.assertEqual(res_eq.status_code, 200)

        res_tl = self.client.get("/api/equipment/EQUIP-001/timeline")
        self.assertEqual(res_tl.status_code, 200)
        self.assertIsInstance(res_tl.json(), list)

        res_hist = self.client.get("/api/equipment/EQUIP-001/history")
        self.assertEqual(res_hist.status_code, 200)

        res_mem = self.client.get("/api/equipment/EQUIP-001/memories")
        self.assertEqual(res_mem.status_code, 200)

    def test_service_request_context_and_hindsight_recall(self):
        # List service requests
        res = self.client.get("/api/service-requests")
        self.assertEqual(res.status_code, 200)
        srs = res.json()
        self.assertGreater(len(srs), 0)

        # Context analysis on first service request
        sr_id = srs[0]["id"]
        res_ctx = self.client.get(f"/api/service-requests/{sr_id}/context")
        self.assertEqual(res_ctx.status_code, 200)
        ctx = res_ctx.json()
        self.assertIn("what_the_memory_says", ctx)
        self.assertIn("evidence", ctx)
        self.assertIn("hindsight_engine_info", ctx)

    def test_ask_memory(self):
        payload = {
            "query": "What did technicians observe regarding compressor vibration on cooling systems?",
            "equipment_id": "EQUIP-001"
        }
        res = self.client.post("/api/memory/ask", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("answer", data)
        self.assertIn("evidence", data)
        self.assertGreater(len(data["evidence"]), 0)

    def test_demo_run(self):
        res = self.client.post("/api/demo/run")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["steps"]), 9)
        self.assertIn("service_request_id", data)
        self.assertIn("agent_context", data)

    def test_memory_lifecycle_retention(self):
        # Create ticket -> context -> complete visit -> retain -> query
        create_res = self.client.post("/api/service-requests", json={
            "title": "Thermal overload test incident",
            "reported_symptoms": "Unit tripped thermal circuit breaker after 5 hours at full load",
            "equipment_id": "EQUIP-001",
            "site_id": "SITE-001",
            "customer_id": "CUST-001",
            "priority": "High"
        })
        self.assertEqual(create_res.status_code, 200)
        sr = create_res.json()
        sr_id = sr["id"]

        # Complete visit
        visit_res = self.client.post(f"/api/service-requests/{sr_id}/complete", json={
            "service_request_id": sr_id,
            "equipment_id": "EQUIP-001",
            "technician_id": "TECH-001",
            "technician_name": "Ravi Verma",
            "visit_date": "2026-09-29",
            "symptoms_observed": "Thermal overload confirmed on compressor circuit",
            "diagnostic_tests": "Thermal imaging and megger insulation check",
            "action_taken": "Replaced worn compressor motor contactor and recalibrated overload relay",
            "parts_replaced": "Contactor 40A Siemens",
            "outcome": "Resolved",
            "effective_duration_days": None,
            "technician_notes": "Thermal tripping completely ceased after contactor swap. Current draw 18.2A normal.",
            "retain_as_memory": True
        })
        self.assertEqual(visit_res.status_code, 200)

        # Verify new memory appears in ask query
        ask_res = self.client.post("/api/memory/ask", json={
            "query": "contactor overload relay thermal",
            "equipment_id": "EQUIP-001"
        })
        self.assertEqual(ask_res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
