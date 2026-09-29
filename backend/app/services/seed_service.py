"""
SeedService — Populates the database with realistic demo data.

Checks if data already exists (customer count > 0) and skips if so.
Creates: 8 Customers, 12 Sites, 10 Technicians, 30 Equipment units,
         55+ Service Records, 30+ Memory Items, and 1 open Service Request.
"""

import logging
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    Customer,
    Equipment,
    MemoryItem,
    ServiceRecord,
    ServiceRequest,
    Site,
    Technician,
)

logger = logging.getLogger(__name__)


class SeedService:
    @staticmethod
    def seed_all(db: Session) -> bool:
        """
        Seed the database.
        Returns True if seeding was performed, False if skipped.
        """
        if db.query(Customer).count() > 0:
            logger.info("Database already seeded — skipping.")
            return False

        logger.info("Seeding database with demo data...")

        try:
            SeedService._seed_customers(db)
            SeedService._seed_sites(db)
            SeedService._seed_technicians(db)
            SeedService._seed_equipment(db)
            SeedService._seed_service_records(db)
            SeedService._seed_service_requests(db)
            SeedService._seed_memory_items(db)
            db.commit()
            logger.info("Database seeding completed successfully.")
            return True
        except Exception as exc:
            logger.error("Seeding failed: %s", exc, exc_info=True)
            db.rollback()
            raise

    # ------------------------------------------------------------------ #
    # Customers                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_customers(db: Session) -> None:
        customers = [
            Customer(id="CUST-001", name="ABC Manufacturing Co.", industry="Manufacturing",
                     contact_name="Priya Sharma", contact_email="priya@abcmfg.in",
                     phone="+91-40-12345678", sla_level="Platinum",
                     notes="Flagship account. Operates 24/7. Strict SLA compliance required."),
            Customer(id="CUST-002", name="Delhi Metro Rail Corp.", industry="Transportation",
                     contact_name="Rajesh Kumar", contact_email="rajesh@delhimetro.in",
                     phone="+91-11-23456789", sla_level="Gold",
                     notes="Public sector client. Security clearance needed for depot access."),
            Customer(id="CUST-003", name="Reliance Petrochemicals", industry="Petrochemical",
                     contact_name="Amit Patel", contact_email="amit@reliancepetro.in",
                     phone="+91-22-34567890", sla_level="Platinum",
                     notes="ATEX certified engineers only. Permit-to-work mandatory."),
            Customer(id="CUST-004", name="Tata Steel Jamshedpur", industry="Steel Manufacturing",
                     contact_name="Sunita Rao", contact_email="sunita@tatasteel.in",
                     phone="+91-657-4567890", sla_level="Gold",
                     notes="Extreme operating conditions near blast furnaces. Heat-resistant PPE required."),
            Customer(id="CUST-005", name="Infosys Campus Pune", industry="Technology",
                     contact_name="Vikram Singh", contact_email="vikram@infosys.com",
                     phone="+91-20-56789012", sla_level="Silver",
                     notes="Commercial HVAC across multiple buildings. Planned maintenance preferred."),
            Customer(id="CUST-006", name="BHEL Power Systems", industry="Power Generation",
                     contact_name="Deepak Mehta", contact_email="deepak@bhel.in",
                     phone="+91-755-6789012", sla_level="Gold",
                     notes="Critical turbine infrastructure. 4-hour response SLA for Priority 1 faults."),
            Customer(id="CUST-007", name="Mahindra Auto Assembly", industry="Automotive",
                     contact_name="Kavya Nair", contact_email="kavya@mahindra.in",
                     phone="+91-253-7890123", sla_level="Gold",
                     notes="Just-in-time manufacturing. Downtime directly impacts production targets."),
            Customer(id="CUST-008", name="Apollo Hospitals Chennai", industry="Healthcare",
                     contact_name="Dr. Arun Bose", contact_email="arun.bose@apollohospitals.in",
                     phone="+91-44-89012345", sla_level="Platinum",
                     notes="Healthcare critical environment. Any HVAC work in ICU requires infection control protocol."),
        ]
        db.bulk_save_objects(customers)
        db.flush()
        logger.info("Seeded %d customers", len(customers))

    # ------------------------------------------------------------------ #
    # Sites                                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_sites(db: Session) -> None:
        sites = [
            Site(id="SITE-001", customer_id="CUST-001", name="Hyderabad Plant",
                 city="Hyderabad", state="Telangana",
                 operating_environment="Heavy Industrial - High Humidity",
                 access_constraints="Requires permit for Zone B. Safety induction mandatory.",
                 notes="High ambient humidity affects HVAC performance year-round."),
            Site(id="SITE-002", customer_id="CUST-001", name="Pune Assembly Line",
                 city="Pune", state="Maharashtra",
                 operating_environment="Standard Industrial",
                 access_constraints="Badge access required. No lone working.",
                 notes="New facility, equipment installed 2021-2022."),
            Site(id="SITE-003", customer_id="CUST-002", name="Blue Line Depot",
                 city="Delhi", state="Delhi NCR",
                 operating_environment="Tunnel - High Dust",
                 access_constraints="Metro security escort required. No cameras permitted.",
                 notes="Heavy dust accumulation from rail operations. Filters require frequent replacement."),
            Site(id="SITE-004", customer_id="CUST-003", name="Jamnagar Refinery",
                 city="Jamnagar", state="Gujarat",
                 operating_environment="Hazardous - Flammable Zone",
                 access_constraints="ATEX equipment only. Hot work permit required. Full PPE mandatory.",
                 notes="Zone 1 hazardous area. All electrical equipment must be Ex-rated."),
            Site(id="SITE-005", customer_id="CUST-004", name="Blast Furnace Block A",
                 city="Jamshedpur", state="Jharkhand",
                 operating_environment="Extreme Heat - 45C+",
                 access_constraints="Heat-resistant PPE required. Buddy system mandatory.",
                 notes="Ambient temperature regularly exceeds 45°C near furnace. Equipment rated for high temp."),
            Site(id="SITE-006", customer_id="CUST-005", name="Main Campus Building 7",
                 city="Pune", state="Maharashtra",
                 operating_environment="Commercial HVAC",
                 access_constraints="Visitor pass required. Work during off-peak hours preferred.",
                 notes="Occupied commercial building. Noise restrictions 9AM-6PM."),
            Site(id="SITE-007", customer_id="CUST-006", name="Turbine Hall 3",
                 city="Bhopal", state="Madhya Pradesh",
                 operating_environment="Power Generation",
                 access_constraints="Qualified electrical engineer required. Lock-out tag-out mandatory.",
                 notes="330MW turbine generators. Critical to grid stability."),
            Site(id="SITE-008", customer_id="CUST-007", name="Nashik Assembly Plant",
                 city="Nashik", state="Maharashtra",
                 operating_environment="Automotive Assembly",
                 access_constraints="Safety boots and hi-vis vest required. No work during shift changes.",
                 notes="Robotic welding and press lines nearby. EMI may affect sensitive instruments."),
            Site(id="SITE-009", customer_id="CUST-008", name="ICU Wing",
                 city="Chennai", state="Tamil Nadu",
                 operating_environment="Hospital - Critical",
                 access_constraints="Infection control protocol. Minimal noise. Work outside patient hours only.",
                 notes="Life-critical environment. Any HVAC failure triggers emergency escalation."),
            Site(id="SITE-010", customer_id="CUST-003", name="Hazira Gas Terminal",
                 city="Surat", state="Gujarat",
                 operating_environment="Offshore Industrial",
                 access_constraints="Coast Guard clearance required. BOSIET certification for offshore team.",
                 notes="Natural gas handling terminal. Strict leak detection protocols."),
            Site(id="SITE-011", customer_id="CUST-002", name="Airport Express Depot",
                 city="Delhi", state="Delhi NCR",
                 operating_environment="Tunnel - High Vibration",
                 access_constraints="CISF security escort. No electronic devices without clearance.",
                 notes="High vibration environment from frequent train movements."),
            Site(id="SITE-012", customer_id="CUST-001", name="Chennai Distribution Hub",
                 city="Chennai", state="Tamil Nadu",
                 operating_environment="Warehouse - High Temp",
                 access_constraints="Forklift traffic — PPE mandatory.",
                 notes="High ambient temperatures in summer (40°C+). Cooling is critical for stored goods."),
        ]
        db.bulk_save_objects(sites)
        db.flush()
        logger.info("Seeded %d sites", len(sites))

    # ------------------------------------------------------------------ #
    # Technicians                                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_technicians(db: Session) -> None:
        technicians = [
            Technician(id="TECH-001", name="Ravi Shankar", role="Senior HVAC Engineer",
                       email="ravi.shankar@fieldservice.in", phone="+91-9876543210",
                       skills="HVAC,Refrigeration,Compressors,Chillers", years_experience=12),
            Technician(id="TECH-002", name="Priyanka Joshi", role="Electrical Systems Engineer",
                       email="priyanka.joshi@fieldservice.in", phone="+91-9876543211",
                       skills="Electrical,PLC,Control Systems,VFD", years_experience=8),
            Technician(id="TECH-003", name="Mohammed Al-Farsi", role="Industrial Pump Specialist",
                       email="mohammed.alfarsi@fieldservice.in", phone="+91-9876543212",
                       skills="Pumps,Hydraulics,Fluid Systems,Centrifugal Pumps", years_experience=15),
            Technician(id="TECH-004", name="Anjali Krishnan", role="Rotating Equipment Engineer",
                       email="anjali.krishnan@fieldservice.in", phone="+91-9876543213",
                       skills="Turbines,Compressors,Vibration Analysis,Alignment", years_experience=10),
            Technician(id="TECH-005", name="Vikram Malhotra", role="Field Service Generalist",
                       email="vikram.malhotra@fieldservice.in", phone="+91-9876543214",
                       skills="HVAC,Electrical,Mechanical,Commissioning", years_experience=6),
            Technician(id="TECH-006", name="Deepa Nayak", role="Cooling Systems Expert",
                       email="deepa.nayak@fieldservice.in", phone="+91-9876543215",
                       skills="Cooling,Refrigeration,HVAC,Chilled Water Systems", years_experience=11),
            Technician(id="TECH-007", name="Arjun Bhat", role="Boiler & Steam Engineer",
                       email="arjun.bhat@fieldservice.in", phone="+91-9876543216",
                       skills="Boilers,Steam,Heat Exchangers,Pressure Vessels", years_experience=9),
            Technician(id="TECH-008", name="Sunita Reddy", role="Electronics & Controls",
                       email="sunita.reddy@fieldservice.in", phone="+91-9876543217",
                       skills="Electronics,PLC,SCADA,HMI,Instrumentation", years_experience=7),
            Technician(id="TECH-009", name="Kiran Patel", role="Mechanical Systems",
                       email="kiran.patel@fieldservice.in", phone="+91-9876543218",
                       skills="Mechanical,Hydraulics,Gear Systems,Bearings", years_experience=13),
            Technician(id="TECH-010", name="Asha Bhatt", role="Site Safety & Commissioning",
                       email="asha.bhatt@fieldservice.in", phone="+91-9876543219",
                       skills="Safety,Commissioning,Quality,Documentation", years_experience=9),
        ]
        db.bulk_save_objects(technicians)
        db.flush()
        logger.info("Seeded %d technicians", len(technicians))

    # ------------------------------------------------------------------ #
    # Equipment (30 units)                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_equipment(db: Session) -> None:
        equipment_list = [
            # ---- HVAC ----
            Equipment(id="EQUIP-001", name="HVAC-204", category="HVAC",
                      site_id="SITE-001", customer_id="CUST-001",
                      model="Carrier 30XA-300", serial_number="CAR-30XA-2022-0315",
                      installation_date="2022-03-15", status="Degraded Performance",
                      criticality="High", operating_hours=18720,
                      notes="Recurring cooling issues. Compressor showing signs of wear."),
            Equipment(id="EQUIP-003", name="AHU-07", category="HVAC",
                      site_id="SITE-006", customer_id="CUST-005",
                      model="Daikin AHU-7500", serial_number="DAI-AHU-2021-1120",
                      installation_date="2021-11-20", status="Operational",
                      criticality="Medium", operating_hours=14400,
                      notes="Commercial AHU serving open-plan office floors 4-6."),
            Equipment(id="EQUIP-006", name="HVAC-115", category="HVAC",
                      site_id="SITE-009", customer_id="CUST-008",
                      model="Carrier 30XA-150", serial_number="CAR-30XA-2020-0601",
                      installation_date="2020-06-01", status="Operational",
                      criticality="Critical", operating_hours=28800,
                      notes="Critical HVAC for ICU wing. Redundant unit HVAC-116 is backup."),
            Equipment(id="EQUIP-007", name="HVAC-116", category="HVAC",
                      site_id="SITE-009", customer_id="CUST-008",
                      model="Carrier 30XA-150", serial_number="CAR-30XA-2020-0602",
                      installation_date="2020-06-01", status="Operational",
                      criticality="Critical", operating_hours=12000,
                      notes="Backup HVAC for ICU wing. Runs in standby mode."),
            Equipment(id="EQUIP-008", name="AHU-B7-02", category="HVAC",
                      site_id="SITE-002", customer_id="CUST-001",
                      model="Voltas H-Series 5000", serial_number="VOL-H5-2021-0830",
                      installation_date="2021-08-30", status="Operational",
                      criticality="Medium", operating_hours=11520),
            Equipment(id="EQUIP-009", name="HVAC-Chennai-01", category="HVAC",
                      site_id="SITE-012", customer_id="CUST-001",
                      model="Blue Star HVAC-5TR", serial_number="BS-5TR-2022-0901",
                      installation_date="2022-09-01", status="Degraded Performance",
                      criticality="High", operating_hours=8760,
                      notes="Frequent trips due to high ambient temperature in warehouse."),

            # ---- Industrial Pump ----
            Equipment(id="EQUIP-002", name="CWP-12", category="Industrial Pump",
                      site_id="SITE-004", customer_id="CUST-003",
                      model="Grundfos NB 65-200", serial_number="GRU-NB65-2020-0810",
                      installation_date="2020-08-10", status="Operational",
                      criticality="Critical", operating_hours=35040,
                      notes="Cooling water pump for refinery heat exchangers. Critical for process cooling."),
            Equipment(id="EQUIP-010", name="FWP-03", category="Industrial Pump",
                      site_id="SITE-005", customer_id="CUST-004",
                      model="KSB Etanorm 100-200", serial_number="KSB-ET-2019-0301",
                      installation_date="2019-03-01", status="Operational",
                      criticality="High", operating_hours=50400,
                      notes="Feed water pump for blast furnace cooling circuit."),
            Equipment(id="EQUIP-011", name="CWP-Hazira-01", category="Industrial Pump",
                      site_id="SITE-010", customer_id="CUST-003",
                      model="Sulzer APP22-80", serial_number="SUL-APP-2021-0601",
                      installation_date="2021-06-01", status="Under Service",
                      criticality="Critical", operating_hours=21900,
                      notes="Seawater cooling pump for gas terminal. Corrosion-resistant alloy."),
            Equipment(id="EQUIP-012", name="WTP-Metro-03", category="Industrial Pump",
                      site_id="SITE-003", customer_id="CUST-002",
                      model="Grundfos CM 10-4", serial_number="GRU-CM10-2020-1101",
                      installation_date="2020-11-01", status="Operational",
                      criticality="Medium", operating_hours=26280),

            # ---- Compressor ----
            Equipment(id="EQUIP-004", name="COMP-A3", category="Compressor",
                      site_id="SITE-005", customer_id="CUST-004",
                      model="Atlas Copco GA90", serial_number="AC-GA90-2019-0512",
                      installation_date="2019-05-12", status="Under Service",
                      criticality="Critical", operating_hours=52560,
                      notes="Air compressor for blast furnace control systems. Recurring bearing issues."),
            Equipment(id="EQUIP-013", name="COMP-Refinery-02", category="Compressor",
                      site_id="SITE-004", customer_id="CUST-003",
                      model="Ingersoll Rand ML37", serial_number="IR-ML37-2018-0901",
                      installation_date="2018-09-01", status="Operational",
                      criticality="Critical", operating_hours=63072,
                      notes="Process gas compressor. ATEX certified."),
            Equipment(id="EQUIP-014", name="COMP-Nashik-01", category="Compressor",
                      site_id="SITE-008", customer_id="CUST-007",
                      model="Atlas Copco GA55", serial_number="AC-GA55-2020-0601",
                      installation_date="2020-06-01", status="Operational",
                      criticality="High", operating_hours=31200),

            # ---- Boiler ----
            Equipment(id="EQUIP-005", name="BLRM-01", category="Boiler",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="Thermax RIB-500", serial_number="THX-RIB-2018-0901",
                      installation_date="2018-09-01", status="Operational",
                      criticality="Critical", operating_hours=62400,
                      notes="500 kW industrial boiler for turbine steam generation."),
            Equipment(id="EQUIP-015", name="BLRM-02", category="Boiler",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="Thermax RIB-500", serial_number="THX-RIB-2019-0301",
                      installation_date="2019-03-01", status="Operational",
                      criticality="Critical", operating_hours=55200),
            Equipment(id="EQUIP-016", name="BLRM-Steel-01", category="Boiler",
                      site_id="SITE-005", customer_id="CUST-004",
                      model="ISGEC Cochran WT-750", serial_number="ISG-WT-2017-1101",
                      installation_date="2017-11-01", status="Degraded Performance",
                      criticality="High", operating_hours=79200,
                      notes="Ageing boiler showing pressure inconsistency. Replacement planned for Q2."),

            # ---- Turbine ----
            Equipment(id="EQUIP-017", name="TRB-GEN-01", category="Turbine",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="Siemens SST-300", serial_number="SIE-SST300-2015-0601",
                      installation_date="2015-06-01", status="Operational",
                      criticality="Critical", operating_hours=96360,
                      notes="110 MW steam turbine generator. Last major overhaul 2023."),
            Equipment(id="EQUIP-018", name="TRB-GEN-02", category="Turbine",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="Siemens SST-300", serial_number="SIE-SST300-2015-0602",
                      installation_date="2015-06-01", status="Operational",
                      criticality="Critical", operating_hours=94320),

            # ---- Hydraulic Press ----
            Equipment(id="EQUIP-019", name="HYD-PRESS-01", category="Hydraulic Press",
                      site_id="SITE-008", customer_id="CUST-007",
                      model="Schuler 1000T Hydraulic Press", serial_number="SCH-1000T-2018-0301",
                      installation_date="2018-03-01", status="Operational",
                      criticality="High", operating_hours=41600,
                      notes="Body panel stamping press. 1000-tonne capacity."),
            Equipment(id="EQUIP-020", name="HYD-PRESS-02", category="Hydraulic Press",
                      site_id="SITE-008", customer_id="CUST-007",
                      model="Schuler 800T Hydraulic Press", serial_number="SCH-800T-2019-0601",
                      installation_date="2019-06-01", status="Degraded Performance",
                      criticality="High", operating_hours=36400,
                      notes="Pressure drops observed intermittently. Seal inspection overdue."),
            Equipment(id="EQUIP-021", name="HYD-UNIT-Metro-01", category="Hydraulic Press",
                      site_id="SITE-011", customer_id="CUST-002",
                      model="Parker HPU-250", serial_number="PAR-HPU-2019-0901",
                      installation_date="2019-09-01", status="Operational",
                      criticality="Medium", operating_hours=30660),

            # ---- Cooling Tower ----
            Equipment(id="EQUIP-022", name="CT-REF-01", category="Cooling Tower",
                      site_id="SITE-004", customer_id="CUST-003",
                      model="SPX Cooling Tower CT-500", serial_number="SPX-CT500-2018-1101",
                      installation_date="2018-11-01", status="Operational",
                      criticality="High", operating_hours=63072,
                      notes="Process cooling tower for main distillation column."),
            Equipment(id="EQUIP-023", name="CT-Steel-01", category="Cooling Tower",
                      site_id="SITE-005", customer_id="CUST-004",
                      model="BACT Counterflow CT-300", serial_number="BAC-CT300-2019-0601",
                      installation_date="2019-06-01", status="Operational",
                      criticality="High", operating_hours=52560,
                      notes="Scale buildup observed in 2024 Q3. Chemical dosing adjusted."),
            Equipment(id="EQUIP-024", name="CT-Power-01", category="Cooling Tower",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="SPX Marley NC 8000", serial_number="SPX-NC8K-2016-0401",
                      installation_date="2016-04-01", status="Operational",
                      criticality="Critical", operating_hours=88320),

            # ---- Generator ----
            Equipment(id="EQUIP-025", name="GEN-BACKUP-01", category="Generator",
                      site_id="SITE-009", customer_id="CUST-008",
                      model="Cummins C1100D5", serial_number="CUM-C1100-2020-0301",
                      installation_date="2020-03-01", status="Operational",
                      criticality="Critical", operating_hours=8760,
                      notes="Hospital backup generator. Tested monthly. Auto-transfer switch connected."),
            Equipment(id="EQUIP-026", name="GEN-BHEL-01", category="Generator",
                      site_id="SITE-007", customer_id="CUST-006",
                      model="BHEL TG-330", serial_number="BHL-TG330-2015-0601",
                      installation_date="2015-06-01", status="Operational",
                      criticality="Critical", operating_hours=96360),
            Equipment(id="EQUIP-027", name="GEN-Infosys-01", category="Generator",
                      site_id="SITE-006", customer_id="CUST-005",
                      model="Kirloskar 500 kVA", serial_number="KIR-500-2019-0901",
                      installation_date="2019-09-01", status="Operational",
                      criticality="Medium", operating_hours=15600),

            # ---- Additional HVAC / mixed ----
            Equipment(id="EQUIP-028", name="FCU-Block-A-01", category="HVAC",
                      site_id="SITE-001", customer_id="CUST-001",
                      model="Voltas FCU-2TR", serial_number="VOL-FCU-2022-0601",
                      installation_date="2022-06-01", status="Operational",
                      criticality="Low", operating_hours=7200),
            Equipment(id="EQUIP-029", name="COMP-Delhi-01", category="Compressor",
                      site_id="SITE-003", customer_id="CUST-002",
                      model="Elgi EG 37", serial_number="ELG-EG37-2021-0301",
                      installation_date="2021-03-01", status="Operational",
                      criticality="Medium", operating_hours=21900),
            Equipment(id="EQUIP-030", name="BLRM-Chennai-01", category="Boiler",
                      site_id="SITE-012", customer_id="CUST-001",
                      model="Forbes Marshall FB-200", serial_number="FM-FB200-2021-1101",
                      installation_date="2021-11-01", status="Operational",
                      criticality="Medium", operating_hours=18000,
                      notes="Steam boiler for distribution hub process heating."),
        ]
        db.bulk_save_objects(equipment_list)
        db.flush()
        logger.info("Seeded %d equipment units", len(equipment_list))

    # ------------------------------------------------------------------ #
    # Service Records (55+)                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_service_records(db: Session) -> None:  # noqa: C901
        records = [
            # ============================================================
            # EQUIP-001 (HVAC-204) — intentional recurring pattern (3 visits)
            # ============================================================
            ServiceRecord(
                id="SREC-001", equipment_id="EQUIP-001",
                technician_id="TECH-001", technician_name="Ravi Shankar",
                visit_date="2025-04-10",
                symptoms_observed=(
                    "Cooling performance dropped 40%. Unit struggling to maintain setpoint of 22°C. "
                    "Warm air from supply grilles. Customer complaints from building staff."
                ),
                diagnostic_tests=(
                    "Checked refrigerant levels, inspected air filters, measured airflow velocity, "
                    "ran compressor amp draw test."
                ),
                action_taken=(
                    "Replaced dirty air filters. Cleaned condenser coils with coil cleaner. "
                    "Topped up refrigerant by 200g. Reset controller."
                ),
                parts_replaced="Air filters x4",
                outcome="Resolved",
                effective_duration_days=45,
                technician_notes=(
                    "Unit had heavily clogged filters — clearly not on proper maintenance schedule. "
                    "Worth watching compressor — heard slight rattle at startup. "
                    "Ambient temp in equipment room was 38°C which is above recommended 35°C max."
                ),
            ),
            ServiceRecord(
                id="SREC-002", equipment_id="EQUIP-001",
                technician_id="TECH-006", technician_name="Deepa Nayak",
                visit_date="2025-05-25",
                symptoms_observed=(
                    "Cooling performance degraded again. Temperature setpoint not being met. "
                    "Noise from compressor section. Supply air temp 4°C above setpoint."
                ),
                diagnostic_tests=(
                    "Full refrigerant circuit inspection. Compressor vibration test using portable analyser. "
                    "Checked TXV valve operation with superheat measurement."
                ),
                action_taken=(
                    "Replaced TXV valve that was partially stuck open causing poor superheat control. "
                    "Adjusted refrigerant charge. Cleaned evaporator coil."
                ),
                parts_replaced="TXV Valve",
                outcome="Temporarily Resolved",
                effective_duration_days=38,
                technician_notes=(
                    "Compressor vibration is concerning — 4.2 mm/s RMS at 1x running speed, above 3.5 mm/s alarm threshold. "
                    "Could be bearing wear. Issue will likely return. "
                    "Client should plan for compressor overhaul. "
                    "Also noted high ambient temperature (38°C) in equipment room — poor ventilation is accelerating degradation."
                ),
            ),
            ServiceRecord(
                id="SREC-003", equipment_id="EQUIP-001",
                technician_id="TECH-001", technician_name="Ravi Shankar",
                visit_date="2025-07-02",
                symptoms_observed=(
                    "Unit completely failed to cool. Compressor tripping on high pressure fault. "
                    "All zones at ambient temperature. Building temperature 32°C."
                ),
                diagnostic_tests=(
                    "Found refrigerant leak at evaporator coil joint. "
                    "High pressure test (held at 400 PSI). "
                    "Megger test on compressor motor windings — readings normal (>100 MΩ). "
                    "Vibration at compressor: 6.1 mm/s RMS — critical level."
                ),
                action_taken=(
                    "Repaired refrigerant leak with brazing. Re-pressurized system. "
                    "Reset high pressure fault. Ran unit in test mode for 2 hours."
                ),
                parts_replaced="Copper pipe joint, Schrader valve",
                outcome="Temporarily Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "This is the third visit for similar issues. The root cause appears to be an ageing compressor. "
                    "Each fix is temporary. Strongly recommend compressor replacement before next summer season. "
                    "Compressor is showing bearing wear on vibration analysis (6.1 mm/s vs 2.5 mm/s baseline). "
                    "Told site manager — they said budget approval needed. "
                    "Risk: if compressor fails completely, building will be without cooling for 2-3 weeks (lead time for replacement)."
                ),
            ),

            # ============================================================
            # EQUIP-002 (CWP-12) — pump cavitation recurring pattern
            # ============================================================
            ServiceRecord(
                id="SREC-004", equipment_id="EQUIP-002",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-02-14",
                symptoms_observed=(
                    "Pump making loud rattling/crackling noise. Flow rate dropped 35%. "
                    "Pressure fluctuating between 3.5-5.0 bar (normal: 4.8 bar stable)."
                ),
                diagnostic_tests=(
                    "Measured suction pressure: 0.15 bar (below NPSH required of 0.4 bar). "
                    "Inspected inlet strainer — found 60% blocked with debris. "
                    "Impeller inspection showed pitting on leading edges."
                ),
                action_taken=(
                    "Cleaned inlet strainer. Replaced worn impeller. "
                    "Adjusted pump speed via VFD to match system curve."
                ),
                parts_replaced="Impeller (stainless steel), Inlet strainer basket",
                outcome="Resolved",
                effective_duration_days=90,
                technician_notes=(
                    "Classic cavitation damage on impeller. Inlet strainer must be checked monthly. "
                    "Recommend increasing strainer mesh size to reduce blockage frequency."
                ),
            ),
            ServiceRecord(
                id="SREC-005", equipment_id="EQUIP-002",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-05-15",
                symptoms_observed=(
                    "Cavitation noise returned. Flow rate at 70% of rated. Bearing temperature elevated (68°C vs 55°C normal)."
                ),
                diagnostic_tests=(
                    "Suction pressure back to 0.18 bar. Strainer partially blocked again. "
                    "Vibration analysis: elevated bearing frequencies."
                ),
                action_taken=(
                    "Cleaned strainer. Replaced bearing set. Increased VFD minimum speed."
                ),
                parts_replaced="Bearing set (Drive-end and Non-drive-end)",
                outcome="Temporarily Resolved",
                effective_duration_days=60,
                technician_notes=(
                    "Strainer is blocking again after only 90 days. "
                    "Root cause is likely debris from the deteriorating pipeline upstream. "
                    "Recommend pipeline inspection and possible installation of automatic self-cleaning strainer."
                ),
            ),
            ServiceRecord(
                id="SREC-006", equipment_id="EQUIP-002",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-07-20",
                symptoms_observed=(
                    "Flow completely stopped. Pump seized. High current draw on motor."
                ),
                diagnostic_tests=(
                    "Found impeller completely corroded through. Shaft seal failed. "
                    "Process liquid had entered bearing housing."
                ),
                action_taken=(
                    "Emergency replacement of impeller, shaft seal, and bearings. "
                    "Flushed and refilled bearing housing."
                ),
                parts_replaced="Impeller, Shaft seal, Bearing set, Bearing housing gasket",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "This is the third major intervention in 6 months. "
                    "Recommend upgrading to duplex pump arrangement — one pump running, one standby. "
                    "Current single-pump design is a single point of failure for refinery cooling."
                ),
            ),

            # ============================================================
            # EQUIP-004 (COMP-A3) — compressor bearing failures
            # ============================================================
            ServiceRecord(
                id="SREC-007", equipment_id="EQUIP-004",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2024-11-08",
                symptoms_observed=(
                    "Abnormal noise from compressor — metallic grinding. Outlet pressure dropping. "
                    "Oil consumption increased (1L/day vs normal 0.1L/week)."
                ),
                diagnostic_tests=(
                    "Vibration spectrum analysis: clear bearing fault frequency at 6.2x running speed. "
                    "Oil sample analysis: iron content 180 ppm (normal <20 ppm). "
                    "Inlet filter condition: acceptable."
                ),
                action_taken=(
                    "Replaced main drive bearing and thrust bearing. "
                    "Flushed oil system and refilled with synthetic lubricant. "
                    "Replaced oil filter."
                ),
                parts_replaced="Main drive bearing, Thrust bearing, Oil filter",
                outcome="Resolved",
                effective_duration_days=60,
                technician_notes=(
                    "Bearing failure likely caused by oil contamination. "
                    "Oil analysis shows elevated iron and copper particles indicating internal wear. "
                    "Compressor has 52,000+ hours — consider major overhaul at next planned shutdown."
                ),
            ),
            ServiceRecord(
                id="SREC-008", equipment_id="EQUIP-004",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-01-12",
                symptoms_observed=(
                    "Bearing noise returned. Pressure slightly low. High vibration on startup."
                ),
                diagnostic_tests=(
                    "New bearing showing premature wear — oil analysis: metallic particles at 95 ppm. "
                    "Found oil cooler partially blocked causing high oil temperature."
                ),
                action_taken="Replaced bearings again. Cleaned oil cooler. Replaced oil.",
                parts_replaced="Bearing set, Oil, Oil cooler cleaning",
                outcome="Temporarily Resolved",
                effective_duration_days=45,
                technician_notes=(
                    "Bearings failing prematurely because oil cooler is underperforming — "
                    "high oil temperature (92°C vs 70°C normal) is degrading lubricant. "
                    "Root cause is oil cooler fouling from blast furnace dust ingress into lube system."
                ),
            ),
            ServiceRecord(
                id="SREC-009", equipment_id="EQUIP-004",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-02-28",
                symptoms_observed=(
                    "Complete compressor failure. Seized. Production line stopped."
                ),
                diagnostic_tests=(
                    "Bearing completely disintegrated. Shaft scoring found. "
                    "Compressor is non-operational."
                ),
                action_taken=(
                    "Compressor taken offline for major overhaul. "
                    "Temporary compressor hired. Shaft, bearings, seals replaced. "
                    "Oil cooler replaced with upgraded model."
                ),
                parts_replaced="Shaft, Full bearing set, All seals, Oil cooler (upgraded)",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Full overhaul completed. Root cause: oil cooler fouling leading to high oil temp → bearing degradation. "
                    "New oil cooler has larger surface area and better dust exclusion. "
                    "Implemented daily oil temperature monitoring. Should stabilise now."
                ),
            ),

            # ============================================================
            # EQUIP-005 (BLRM-01) — boiler pressure relief issues
            # ============================================================
            ServiceRecord(
                id="SREC-010", equipment_id="EQUIP-005",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-01-20",
                symptoms_observed=(
                    "Safety relief valve lifting intermittently at working pressure. "
                    "Steam pressure fluctuating ±0.5 bar around setpoint."
                ),
                diagnostic_tests=(
                    "Tested SRV set pressure — found lifting at 9.8 bar instead of 10.5 bar (set point). "
                    "Pressure controller calibration check — within tolerance. "
                    "Burner firing rate analysis."
                ),
                action_taken=(
                    "Replaced safety relief valve with new calibrated unit. "
                    "Adjusted burner modulation settings."
                ),
                parts_replaced="Safety Relief Valve (SRV)",
                outcome="Resolved",
                effective_duration_days=120,
                technician_notes=(
                    "SRV had drifted low — probably due to seat corrosion in the steam environment. "
                    "Replace SRV every 12 months as per BS EN 4126 recommendation."
                ),
            ),
            ServiceRecord(
                id="SREC-011", equipment_id="EQUIP-005",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-05-22",
                symptoms_observed=(
                    "Steam consumption increased 15%. Economiser outlet temperature below expected."
                ),
                diagnostic_tests=(
                    "Flue gas analysis: O2 at 7% (target 3-4%). "
                    "Economiser fouled with soot. Combustion efficiency calculated at 79% (target 88%)."
                ),
                action_taken=(
                    "Cleaned economiser tubes. Adjusted air-fuel ratio. "
                    "Replaced O2 sensor in flue gas analyser."
                ),
                parts_replaced="O2 sensor",
                outcome="Resolved",
                effective_duration_days=180,
                technician_notes=(
                    "Combustion efficiency restored to 88.5%. Soot buildup from incomplete combustion. "
                    "Recommend annual economiser cleaning in maintenance schedule."
                ),
            ),

            # ============================================================
            # EQUIP-022 (CT-REF-01) — cooling tower scaling
            # ============================================================
            ServiceRecord(
                id="SREC-012", equipment_id="EQUIP-022",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-03-05",
                symptoms_observed=(
                    "Cooling efficiency dropped. Approach temperature increased from 5°C to 12°C. "
                    "White deposits on fill media and basin."
                ),
                diagnostic_tests=(
                    "Water analysis: hardness 850 ppm (target <300), TDS 4200 ppm (target <2000). "
                    "Fill media inspection — 40% of area blocked by scale deposits."
                ),
                action_taken=(
                    "Acid descale treatment. Replaced 30% of blocked fill media. "
                    "Adjusted chemical dosing programme. Increased blowdown frequency."
                ),
                parts_replaced="Fill media sections x3",
                outcome="Resolved",
                effective_duration_days=90,
                technician_notes=(
                    "Severe calcium carbonate scaling due to high hardness make-up water. "
                    "Chemical treatment programme was undersized for current operating conditions. "
                    "Recommend installing water softener or online dosing monitor."
                ),
            ),
            ServiceRecord(
                id="SREC-013", equipment_id="EQUIP-022",
                technician_id="TECH-010", technician_name="Asha Bhatt",
                visit_date="2025-06-15",
                symptoms_observed=(
                    "Scaling returned. Approach temperature at 10°C. Basin inspection shows new deposits."
                ),
                diagnostic_tests=(
                    "Water hardness now 650 ppm — improved but still high. "
                    "Chemical dosing pump found to have failed — no biocide dosing for 3 weeks."
                ),
                action_taken=(
                    "Replaced failed dosing pump. Shock chlorination treatment. "
                    "Partial acid descale."
                ),
                parts_replaced="Chemical dosing pump",
                outcome="Temporarily Resolved",
                effective_duration_days=60,
                technician_notes=(
                    "The dosing pump failure caused a 3-week gap in chemical treatment — leading to rapid scaling. "
                    "Need a redundant dosing pump or at minimum a pump failure alarm linked to site SCADA."
                ),
            ),

            # ============================================================
            # EQUIP-020 (HYD-PRESS-02) — hydraulic pressure drops
            # ============================================================
            ServiceRecord(
                id="SREC-014", equipment_id="EQUIP-020",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-04-20",
                symptoms_observed=(
                    "Press not reaching full tonnage. Hydraulic pressure drops under load. "
                    "Cycle time increased by 30%."
                ),
                diagnostic_tests=(
                    "Pressure test: system reached 280 bar instead of rated 350 bar. "
                    "Relief valve set at 300 bar — checked OK. "
                    "Pump efficiency test — volumetric efficiency only 68% (normal >85%)."
                ),
                action_taken=(
                    "Replaced worn hydraulic pump internals (vane kit). "
                    "Flushed hydraulic fluid — found high particle count (NAS 9 vs NAS 6 target). "
                    "Replaced hydraulic filter."
                ),
                parts_replaced="Pump vane kit, Hydraulic filter, 120L hydraulic fluid",
                outcome="Temporarily Resolved",
                effective_duration_days=50,
                technician_notes=(
                    "Hydraulic fluid contamination is the root cause. NAS 9 particle level indicates "
                    "internal wear debris circulating. Need to find the source of contamination — "
                    "cylinder seal wear is suspect. Recommend cylinder barrel inspection."
                ),
            ),
            ServiceRecord(
                id="SREC-015", equipment_id="EQUIP-020",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-06-10",
                symptoms_observed=(
                    "Pressure drop returned. Oil leaking from cylinder seal area."
                ),
                diagnostic_tests=(
                    "Cylinder seal inspection — both primary and secondary seals failed. "
                    "Cylinder bore showed scoring from particulate contamination."
                ),
                action_taken=(
                    "Replaced cylinder seals and wipers. Honed cylinder bore. "
                    "Full hydraulic fluid change with high-filtration flush."
                ),
                parts_replaced="Cylinder seal kit, Cylinder wiper seals",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Cylinder seals were the root cause of contamination. Scoring on bore confirmed. "
                    "After honing and new seals, particle count at NAS 5. Should be stable now. "
                    "Recommend 3-monthly oil sample analysis."
                ),
            ),

            # ============================================================
            # EQUIP-006 (HVAC-115 ICU) — critical HVAC incidents
            # ============================================================
            ServiceRecord(
                id="SREC-016", equipment_id="EQUIP-006",
                technician_id="TECH-006", technician_name="Deepa Nayak",
                visit_date="2025-03-12",
                symptoms_observed=(
                    "Supply air temperature 3°C above setpoint. Humidity at 65% (target 50-55%). "
                    "ICU backup unit HVAC-116 activated automatically."
                ),
                diagnostic_tests=(
                    "Refrigerant circuit inspection: subcooling only 2°C (target 8-10°C). "
                    "Condenser fan motor: reduced airflow — motor bearing noisy."
                ),
                action_taken=(
                    "Replaced condenser fan motor bearing. Topped refrigerant. "
                    "Recalibrated humidity sensor."
                ),
                parts_replaced="Condenser fan motor bearing x2, Humidity sensor",
                outcome="Resolved",
                effective_duration_days=150,
                technician_notes=(
                    "Critical unit — backup activated for 4 hours during repair. "
                    "Condenser fan bearing was worn — common failure mode at 28,000+ hours. "
                    "Recommend proactive replacement of HVAC-116 condenser bearings at next scheduled maintenance."
                ),
            ),
            ServiceRecord(
                id="SREC-017", equipment_id="EQUIP-006",
                technician_id="TECH-001", technician_name="Ravi Shankar",
                visit_date="2025-08-01",
                symptoms_observed=(
                    "ICU unit tripped on phase imbalance fault. Backup unit took over."
                ),
                diagnostic_tests=(
                    "Electrical panel inspection — found loose connection on L2 phase. "
                    "Phase voltages: L1=413V, L2=387V, L3=411V — L2 significantly low."
                ),
                action_taken=(
                    "Tightened all electrical connections. Load balanced. Reset fault."
                ),
                parts_replaced="None",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Loose connection likely loosened by vibration over time. "
                    "All electrical connections should be re-torqued annually in vibration-prone environments."
                ),
            ),

            # ============================================================
            # EQUIP-017 (TRB-GEN-01) — turbine vibration
            # ============================================================
            ServiceRecord(
                id="SREC-018", equipment_id="EQUIP-017",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-02-10",
                symptoms_observed=(
                    "Shaft vibration increased to 85 µm (alarm at 75 µm). "
                    "Running at 3000 rpm. Vibration increases under load."
                ),
                diagnostic_tests=(
                    "Orbit plot analysis: 1x vibration dominant — unbalance signature. "
                    "Bearing temperatures normal. Lube oil pressure and temperature normal."
                ),
                action_taken=(
                    "Trim balance correction — added balance weights to LP rotor. "
                    "Vibration reduced to 42 µm."
                ),
                parts_replaced="Balance weights",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Unbalance likely caused by blade erosion over time. "
                    "Monitor vibration trend monthly. Next planned outage: blade inspection recommended."
                ),
            ),

            # ============================================================
            # EQUIP-025 (GEN-BACKUP-01) — generator maintenance
            # ============================================================
            ServiceRecord(
                id="SREC-019", equipment_id="EQUIP-025",
                technician_id="TECH-002", technician_name="Priyanka Joshi",
                visit_date="2025-04-05",
                symptoms_observed=(
                    "Monthly load test failed — generator failed to start on auto-transfer. "
                    "Hospital on mains power only — emergency situation."
                ),
                diagnostic_tests=(
                    "Battery voltage: 23.1V (minimum 24V required). Battery internal resistance high. "
                    "Fuel level: 78% — OK. Engine: turned over manually — starts fine."
                ),
                action_taken=(
                    "Replaced starter batteries. Tested auto-transfer switch operation. "
                    "Load tested at 80% rated load for 30 minutes — passed."
                ),
                parts_replaced="Starter batteries x2 (12V 180Ah)",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Batteries were 5 years old — past recommended 3-4 year replacement interval. "
                    "Hospital should have battery replacement on a fixed 3-year schedule."
                ),
            ),

            # ============================================================
            # EQUIP-010 (FWP-03) — feed water pump
            # ============================================================
            ServiceRecord(
                id="SREC-020", equipment_id="EQUIP-010",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-03-18",
                symptoms_observed=(
                    "Flow rate at 65% of rated. Pump vibrating excessively. "
                    "Bearing temperature 82°C (limit 75°C)."
                ),
                diagnostic_tests=(
                    "Vibration analysis: imbalance at 1x, bearing defect frequencies at 4.8x. "
                    "Seal leak detected — hot water leaking at shaft seal."
                ),
                action_taken=(
                    "Replaced mechanical seal. Replaced drive-end bearing. "
                    "Dynamic balance check performed in-situ."
                ),
                parts_replaced="Mechanical seal, Drive-end bearing",
                outcome="Resolved",
                effective_duration_days=120,
                technician_notes=(
                    "Seal life was only 2.5 years — below expected 5 years. "
                    "High temperature process fluid (>80°C) accelerates seal degradation. "
                    "Consider upgrading to high-temperature seal grade."
                ),
            ),

            # ============================================================
            # EQUIP-009 (HVAC-Chennai-01) — warehouse HVAC
            # ============================================================
            ServiceRecord(
                id="SREC-021", equipment_id="EQUIP-009",
                technician_id="TECH-005", technician_name="Vikram Malhotra",
                visit_date="2025-05-08",
                symptoms_observed=(
                    "Unit trips on high pressure fault. Condenser area very hot — "
                    "ambient temp 42°C outside. Cannot maintain setpoint."
                ),
                diagnostic_tests=(
                    "Condenser pressure 28 bar (limit 25 bar). Condenser coil fouled with dust. "
                    "Ambient temperature at condenser inlet 42°C — above rated 40°C."
                ),
                action_taken=(
                    "High-pressure clean of condenser coil. Installed reflective shade over condenser. "
                    "Reset high pressure fault."
                ),
                parts_replaced="None",
                outcome="Temporarily Resolved",
                effective_duration_days=30,
                technician_notes=(
                    "Unit is operating near its thermal design limit in Chennai summer. "
                    "Shade structure helps marginally. Long-term fix would be to add condenser fan boosters "
                    "or relocate condenser to shaded area. Customer should consider unit upgrade."
                ),
            ),
            ServiceRecord(
                id="SREC-022", equipment_id="EQUIP-009",
                technician_id="TECH-005", technician_name="Vikram Malhotra",
                visit_date="2025-06-08",
                symptoms_observed=(
                    "High pressure fault again. Shade structure was removed by site during roof maintenance work."
                ),
                diagnostic_tests="Condenser pressure 29 bar. Coil clean — shade removed.",
                action_taken=(
                    "Reinstalled shade. Added permanent fixing brackets. "
                    "Instructed site team not to remove without notifying HVAC team."
                ),
                parts_replaced="Shade structure fixings",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Site team removed our shade structure during maintenance. "
                    "Need to label shade structure and add to site asset register."
                ),
            ),

            # ============================================================
            # EQUIP-013 (COMP-Refinery-02) — process compressor
            # ============================================================
            ServiceRecord(
                id="SREC-023", equipment_id="EQUIP-013",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2024-10-15",
                symptoms_observed=(
                    "Inter-stage pressure ratio out of spec. Stage 2 outlet pressure 15% low."
                ),
                diagnostic_tests=(
                    "Inter-stage valve inspection: Stage 2 inlet valve spring broken. "
                    "Valve plate showing erosion wear."
                ),
                action_taken=(
                    "Replaced Stage 2 inlet valve assembly. Replaced valve plates on all stages as preventive measure."
                ),
                parts_replaced="Stage 2 inlet valve, Valve plates x6",
                outcome="Resolved",
                effective_duration_days=365,
                technician_notes=(
                    "Valve spring fatigue is normal at 63,000 hours. "
                    "Valve replacement on all stages proactively — good practice to prevent future unplanned outages."
                ),
            ),

            # ============================================================
            # EQUIP-016 (BLRM-Steel-01) — ageing boiler
            # ============================================================
            ServiceRecord(
                id="SREC-024", equipment_id="EQUIP-016",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-01-08",
                symptoms_observed=(
                    "Steam pressure inconsistency — cycling between 8.5-10.0 bar. "
                    "SRV chattering. Customer reported frequent alarms."
                ),
                diagnostic_tests=(
                    "Boiler internals inspection — found scale deposits on waterside surface. "
                    "Scale thickness up to 3mm on heating surface. "
                    "Burner inspection — combustion air damper sticking."
                ),
                action_taken=(
                    "Acid descaling treatment (2-day process). "
                    "Repaired combustion air damper actuator."
                ),
                parts_replaced="Damper actuator",
                outcome="Temporarily Resolved",
                effective_duration_days=60,
                technician_notes=(
                    "Boiler is 9 years old — scale is accumulating faster now. "
                    "Vessel inspection due — request statutory inspection to assess tube condition. "
                    "Replacement should be planned for next year if tube inspection finds wall thinning."
                ),
            ),
            ServiceRecord(
                id="SREC-025", equipment_id="EQUIP-016",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-03-15",
                symptoms_observed=(
                    "Pressure fluctuation returned. Burner lockout fault — 3 times in one day."
                ),
                diagnostic_tests=(
                    "Flame detector dirty — UV cell reading 30% of normal signal. "
                    "Gas pressure at burner inlet 5% below min spec."
                ),
                action_taken=(
                    "Cleaned flame detector UV cell. Gas pressure regulator adjusted."
                ),
                parts_replaced="None",
                outcome="Temporarily Resolved",
                effective_duration_days=45,
                technician_notes=(
                    "Boiler is becoming increasingly unreliable. "
                    "Multiple systems showing wear simultaneously — typical of ageing equipment. "
                    "Strongly recommend proactive replacement planning."
                ),
            ),

            # ============================================================
            # EQUIP-003 (AHU-07 Infosys) — routine maintenance
            # ============================================================
            ServiceRecord(
                id="SREC-026", equipment_id="EQUIP-003",
                technician_id="TECH-005", technician_name="Vikram Malhotra",
                visit_date="2025-02-20",
                symptoms_observed=(
                    "Planned preventive maintenance visit. No fault reported."
                ),
                diagnostic_tests=(
                    "Filter condition check, belt tension, refrigerant pressure, drain pan inspection."
                ),
                action_taken=(
                    "Replaced air filters. Cleaned drain pan and condensate trap. "
                    "Adjusted belt tension. Lubricated fan bearings."
                ),
                parts_replaced="Air filters x6, Fan belt",
                outcome="Resolved",
                effective_duration_days=180,
                technician_notes=(
                    "Unit in good condition. Running smoothly. "
                    "Refrigerant charge healthy. Fan bearings starting to show slight wear — "
                    "plan replacement at next maintenance visit."
                ),
            ),
            ServiceRecord(
                id="SREC-027", equipment_id="EQUIP-003",
                technician_id="TECH-006", technician_name="Deepa Nayak",
                visit_date="2025-08-18",
                symptoms_observed=(
                    "Planned maintenance. Customer reports slight vibration from AHU — staff can feel it through floor."
                ),
                diagnostic_tests=(
                    "Fan bearing vibration: 3.2 mm/s (alert at 3.5). "
                    "Belt: good condition. Filters: clean (last replaced Feb 25)."
                ),
                action_taken="Proactively replaced fan bearings before failure.",
                parts_replaced="Fan bearings x2",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Good call replacing bearings proactively — would have failed within 2-3 months based on vibration trend."
                ),
            ),

            # ============================================================
            # EQUIP-008 (AHU-B7-02 Pune)
            # ============================================================
            ServiceRecord(
                id="SREC-028", equipment_id="EQUIP-008",
                technician_id="TECH-001", technician_name="Ravi Shankar",
                visit_date="2025-05-10",
                symptoms_observed="Insufficient cooling on assembly line. Workers reporting heat stress.",
                diagnostic_tests="Refrigerant pressure low. Found refrigerant leak at service port.",
                action_taken="Replaced Schrader valve at service port. Recharged refrigerant.",
                parts_replaced="Schrader valve",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes="Simple leak at service port — likely from improper previous gauge connection. Fixed.",
            ),

            # ============================================================
            # EQUIP-011 (CWP-Hazira-01) — seawater pump
            # ============================================================
            ServiceRecord(
                id="SREC-029", equipment_id="EQUIP-011",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-06-01",
                symptoms_observed=(
                    "Pump output significantly reduced. Excessive vibration. Shaft seal leaking seawater."
                ),
                diagnostic_tests=(
                    "Impeller corrosion: lost 15mm of blade tips to corrosion. "
                    "Shaft seal completely degraded. Bearing housing corroded."
                ),
                action_taken=(
                    "Replaced impeller (duplex stainless upgrade). New shaft seal. "
                    "Bearing housing replaced. Applied anti-corrosion coating."
                ),
                parts_replaced="Impeller (upgraded duplex SS), Shaft seal, Bearing housing",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Seawater is extremely aggressive. Duplex stainless steel impeller should last longer "
                    "than previous standard SS. Apply sacrificial anodes to casing — recommend to customer."
                ),
            ),

            # ============================================================
            # EQUIP-019 (HYD-PRESS-01 Nashik)
            # ============================================================
            ServiceRecord(
                id="SREC-030", equipment_id="EQUIP-019",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-04-01",
                symptoms_observed="Hydraulic fluid leak from main cylinder gland seal.",
                diagnostic_tests="Gland seal inspection — seal lip worn through.",
                action_taken="Replaced gland seal. Topped up hydraulic fluid.",
                parts_replaced="Gland seal",
                outcome="Resolved",
                effective_duration_days=365,
                technician_notes="Normal seal wear at 40,000+ hours. Scheduled replacement — no underlying issue.",
            ),

            # ============================================================
            # EQUIP-024 (CT-Power-01) — power plant cooling tower
            # ============================================================
            ServiceRecord(
                id="SREC-031", equipment_id="EQUIP-024",
                technician_id="TECH-010", technician_name="Asha Bhatt",
                visit_date="2025-04-15",
                symptoms_observed=(
                    "Cooling tower fan gearbox making grinding noise. Fan speed reduced."
                ),
                diagnostic_tests=(
                    "Gearbox oil sample: high viscosity, iron content 320 ppm. "
                    "Gear tooth inspection: micropitting on drive pinion."
                ),
                action_taken=(
                    "Replaced gearbox oil. Applied EP additive. "
                    "Adjusted fan pitch angle. Scheduled gearbox replacement for next shutdown."
                ),
                parts_replaced="Gearbox oil",
                outcome="Temporarily Resolved",
                effective_duration_days=90,
                technician_notes=(
                    "Gearbox is at end of life — 10 years old. "
                    "Planned replacement during Q3 planned outage. "
                    "Monitor oil temperature and noise weekly."
                ),
            ),
            ServiceRecord(
                id="SREC-032", equipment_id="EQUIP-024",
                technician_id="TECH-010", technician_name="Asha Bhatt",
                visit_date="2025-07-15",
                symptoms_observed="Gearbox noise increased significantly. Fan barely turning.",
                diagnostic_tests="Gear teeth completely worn. Gearbox seized.",
                action_taken=(
                    "Emergency gearbox replacement. Turbine derated to 60% output during repair."
                ),
                parts_replaced="Fan gearbox complete unit",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes="Gearbox failed earlier than expected — 90 days vs 120 predicted. Should have replaced at April visit.",
            ),

            # ============================================================
            # EQUIP-027 (GEN-Infosys-01) — campus generator
            # ============================================================
            ServiceRecord(
                id="SREC-033", equipment_id="EQUIP-027",
                technician_id="TECH-002", technician_name="Priyanka Joshi",
                visit_date="2025-06-20",
                symptoms_observed=(
                    "Generator AVR (Automatic Voltage Regulator) fault alarm. "
                    "Voltage output unstable during load test."
                ),
                diagnostic_tests=(
                    "AVR output voltage: fluctuating ±8% (limit ±2%). "
                    "Exciter diode bridge: two diodes failed."
                ),
                action_taken=(
                    "Replaced exciter diode bridge. Recalibrated AVR. "
                    "Load tested at 100% rated load — voltage stable ±0.5%."
                ),
                parts_replaced="Exciter diode bridge",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Diode failure is a known failure mode on this generator model after 6+ years. "
                    "Stock spare diode bridge recommended — lead time is 3 weeks."
                ),
            ),

            # ============================================================
            # EQUIP-029 (COMP-Delhi-01) — metro depot compressor
            # ============================================================
            ServiceRecord(
                id="SREC-034", equipment_id="EQUIP-029",
                technician_id="TECH-002", technician_name="Priyanka Joshi",
                visit_date="TECH-2025-06-30",
                symptoms_observed=(
                    "Compressor control panel showing 'screw element temperature high' alarm."
                ),
                diagnostic_tests=(
                    "Oil temperature at element outlet: 110°C (limit 100°C). "
                    "Oil cooler fins blocked with tunnel dust."
                ),
                action_taken=(
                    "High pressure clean of oil cooler fins. Changed oil. "
                    "Replaced thermostatic bypass valve (stuck open)."
                ),
                parts_replaced="Thermostatic bypass valve",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes=(
                    "Tunnel dust is a persistent issue for this site — oil cooler fins block every 3-4 months. "
                    "Recommend adding foam pre-filter on cooler air intake."
                ),
            ),

            # ============================================================
            # EQUIP-030 (BLRM-Chennai-01)
            # ============================================================
            ServiceRecord(
                id="SREC-035", equipment_id="EQUIP-030",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-07-01",
                symptoms_observed="Boiler feed water pump noise. Low water level alarm.",
                diagnostic_tests="Feed pump cavitating — deaerator head too low. Water treatment log reviewed.",
                action_taken=(
                    "Adjusted deaerator level. Descaled feed pump strainer. "
                    "Checked water treatment dosing — biocide concentration low."
                ),
                parts_replaced="None",
                outcome="Resolved",
                effective_duration_days=None,
                technician_notes="Simple operational adjustment. Operator training on deaerator level management recommended.",
            ),

            # ============================================================
            # Additional records for variety (SREC-036 to SREC-055)
            # ============================================================
            ServiceRecord(
                id="SREC-036", equipment_id="EQUIP-014",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-03-22",
                symptoms_observed="Compressor discharge temperature high. Aftercooler not working effectively.",
                diagnostic_tests="Aftercooler fins fouled. Cooling water flow restricted.",
                action_taken="Cleaned aftercooler. Replaced cooling water strainer.",
                parts_replaced="Cooling water strainer",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Typical maintenance issue. Monthly aftercooler inspection recommended."),
            ServiceRecord(
                id="SREC-037", equipment_id="EQUIP-015",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-04-25",
                symptoms_observed="Low steam pressure alarm. Burner modulating incorrectly.",
                diagnostic_tests="Gas pressure modulating valve sticking. Controller output OK.",
                action_taken="Replaced gas modulating valve.",
                parts_replaced="Gas modulating valve",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Valve was sticking at 40% open — causing low firing rate."),
            ServiceRecord(
                id="SREC-038", equipment_id="EQUIP-012",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-05-30",
                symptoms_observed="Pump vibrating. Slight noise at seal area.",
                diagnostic_tests="Mechanical seal showing early wear. Bearing condition acceptable.",
                action_taken="Replaced mechanical seal proactively.",
                parts_replaced="Mechanical seal",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Proactive replacement during tunnel access window. Good timing."),
            ServiceRecord(
                id="SREC-039", equipment_id="EQUIP-021",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-06-12",
                symptoms_observed="Hydraulic unit pressure fluctuating during door operation cycles.",
                diagnostic_tests="Hydraulic accumulator pre-charge pressure low: 80 bar vs 120 bar required.",
                action_taken="Recharged accumulator with nitrogen to 120 bar.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=180,
                technician_notes="Nitrogen pre-charge check should be annual maintenance item."),
            ServiceRecord(
                id="SREC-040", equipment_id="EQUIP-023",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-02-25",
                symptoms_observed="Cooling tower approach temperature elevated. Water treatment alarm.",
                diagnostic_tests="TDS elevated. Fill media partially blocked. Dosing pump running OK.",
                action_taken="Increased blowdown frequency. Partial fill media cleaning.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=120,
                technician_notes="Scale control improving. Chemical dosing programme revised upward 20%."),
            ServiceRecord(
                id="SREC-041", equipment_id="EQUIP-026",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-05-20",
                symptoms_observed="Generator vibration increased. Bearing temperature slightly elevated.",
                diagnostic_tests="1x vibration dominant — rotor unbalance. Bearing temperatures 68°C (limit 75°C).",
                action_taken="Trim balance correction. Tightened rotor endplate bolts.",
                parts_replaced="Balance weights",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Annual trim balance is routine for this machine. Bearings fine."),
            ServiceRecord(
                id="SREC-042", equipment_id="EQUIP-018",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-07-10",
                symptoms_observed="Turbine #2 governor hunting — load oscillating.",
                diagnostic_tests="Governor actuator response time slow. Hydraulic oil low.",
                action_taken="Topped governor hydraulic oil. Recalibrated governor PID parameters.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Governor instability resolved with PID tuning. Monitor for recurrence."),
            ServiceRecord(
                id="SREC-043", equipment_id="EQUIP-028",
                technician_id="TECH-005", technician_name="Vikram Malhotra",
                visit_date="2025-06-15",
                symptoms_observed="FCU not cooling. Fan running but no cold air.",
                diagnostic_tests="Chilled water valve stuck closed. Actuator failed.",
                action_taken="Replaced chilled water valve actuator.",
                parts_replaced="Valve actuator",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Simple actuator failure. Keep spare actuators on truck — common failure."),
            ServiceRecord(
                id="SREC-044", equipment_id="EQUIP-007",
                technician_id="TECH-006", technician_name="Deepa Nayak",
                visit_date="2025-07-20",
                symptoms_observed="Backup HVAC-116 showing refrigerant pressure low after standby mode test.",
                diagnostic_tests="Low refrigerant — slight leak at brazed joint during thermal cycling.",
                action_taken="Repaired brazed joint. Recharged refrigerant. Pressure test 24 hours.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Critical to keep backup unit serviceable. Thermal cycling in standby mode stresses joints — check annually."),
            ServiceRecord(
                id="SREC-045", equipment_id="EQUIP-010",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-07-05",
                symptoms_observed="FWP-03 seal leaking again. Bearing temperature rising.",
                diagnostic_tests="Seal failed after only 4 months. High process temperature identified as degradation cause.",
                action_taken="Replaced seal with upgraded high-temperature PTFE seal.",
                parts_replaced="High-temperature shaft seal (PTFE)",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Standard seal was wrong material spec for 80°C+ process. Upgraded seal should last 5+ years."),
            ServiceRecord(
                id="SREC-046", equipment_id="EQUIP-013",
                technician_id="TECH-008", technician_name="Sunita Reddy",
                visit_date="2025-07-18",
                symptoms_observed="Compressor control panel PLC fault. Compressor not starting.",
                diagnostic_tests="PLC input card fault — lost signal from pressure transmitter.",
                action_taken="Replaced faulty PLC input card. Recalibrated pressure transmitter.",
                parts_replaced="PLC input card",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Humidity in control panel — ATEX gland seals need inspection. Moisture ingress causing PCB corrosion."),
            ServiceRecord(
                id="SREC-047", equipment_id="EQUIP-019",
                technician_id="TECH-009", technician_name="Kiran Patel",
                visit_date="2025-07-22",
                symptoms_observed="Press tonnage still slightly low despite April repair.",
                diagnostic_tests="Pump output now at 95% — minor internal leakage remaining. Acceptable.",
                action_taken="Adjusted relief valve setting slightly. Monitored 50 cycles.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Performance acceptable. Full pump replacement at next annual shutdown."),
            ServiceRecord(
                id="SREC-048", equipment_id="EQUIP-011",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-07-28",
                symptoms_observed="Post-repair vibration check on CWP-Hazira-01.",
                diagnostic_tests="Vibration 1.8 mm/s — excellent. Flow rate at 98% of rated.",
                action_taken="No action required. Site acceptance sign-off.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Excellent result from June repair. Duplex SS impeller performing well."),
            ServiceRecord(
                id="SREC-049", equipment_id="EQUIP-022",
                technician_id="TECH-010", technician_name="Asha Bhatt",
                visit_date="2025-08-10",
                symptoms_observed="Cooling tower fan motor tripping on overload.",
                diagnostic_tests="Fan motor current draw high — blade pitch angle too high after last adjustment.",
                action_taken="Reduced fan blade pitch angle to reduce motor load. Current within limits.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Blade pitch set too aggressively in March visit. Corrected now."),
            ServiceRecord(
                id="SREC-050", equipment_id="EQUIP-006",
                technician_id="TECH-006", technician_name="Deepa Nayak",
                visit_date="2025-09-01",
                symptoms_observed="Routine scheduled maintenance — ICU HVAC-115.",
                diagnostic_tests="All parameters within spec. Refrigerant charge good. Filter clean.",
                action_taken="Replaced UV germicidal lamp. Cleaned drain pan. Lubricated fan bearings.",
                parts_replaced="UV germicidal lamp",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Unit in excellent health. Proactive bearing lubrication to prevent recurrence of March fault."),
            ServiceRecord(
                id="SREC-051", equipment_id="EQUIP-016",
                technician_id="TECH-007", technician_name="Arjun Bhat",
                visit_date="2025-05-01",
                symptoms_observed="Boiler lockout fault — flame failure 4 times in 2 hours.",
                diagnostic_tests="Ignition electrode gap incorrect. Gas valve pilot adjustment needed.",
                action_taken="Reset ignition electrode gap. Adjusted pilot gas pressure.",
                parts_replaced="None",
                outcome="Temporarily Resolved", effective_duration_days=30,
                technician_notes="This boiler is giving constant issues. Recommend replacement — too many faults now."),
            ServiceRecord(
                id="SREC-052", equipment_id="EQUIP-002",
                technician_id="TECH-003", technician_name="Mohammed Al-Farsi",
                visit_date="2025-08-15",
                symptoms_observed="CWP-12 slight noise returning after July repair. Customer concerned.",
                diagnostic_tests="Vibration: 2.1 mm/s — acceptable. Suction pressure OK at 0.42 bar.",
                action_taken="Monitored for 2 hours. No action needed. Reassured customer.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Customer sensitised after previous failures. Unit is actually OK. Set up remote vibration monitoring."),
            ServiceRecord(
                id="SREC-053", equipment_id="EQUIP-004",
                technician_id="TECH-008", technician_name="Sunita Reddy",
                visit_date="2025-08-20",
                symptoms_observed="COMP-A3 SCADA alarm — oil temperature slightly high (78°C vs 70°C target).",
                diagnostic_tests="New oil cooler performing well. High ambient temp (46°C) causing elevated oil temp.",
                action_taken="No mechanical intervention. Increased cooler fan speed via VFD.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Post-overhaul performance monitoring. Oil temp elevated due to extreme ambient. Fan speed increase resolved it."),
            ServiceRecord(
                id="SREC-054", equipment_id="EQUIP-017",
                technician_id="TECH-004", technician_name="Anjali Krishnan",
                visit_date="2025-09-10",
                symptoms_observed="TRB-GEN-01 vibration slightly elevated after 7 months. 48 µm — below alarm.",
                diagnostic_tests="Orbit plot: clean 1x signature. Bearing temps normal.",
                action_taken="No action — within limits. Next trim balance at 6-month interval.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Vibration trending up slowly — schedule next trim balance for March 2026."),
            ServiceRecord(
                id="SREC-055", equipment_id="EQUIP-025",
                technician_id="TECH-002", technician_name="Priyanka Joshi",
                visit_date="2025-09-15",
                symptoms_observed="Generator monthly load test. No fault.",
                diagnostic_tests="Load test at 80% rated: voltage 415V ±0.8%, frequency 50.0Hz. All OK.",
                action_taken="No action. Test log signed.",
                parts_replaced="None",
                outcome="Resolved", effective_duration_days=None,
                technician_notes="Generator healthy after April battery replacement. All systems green."),
        ]

        db.bulk_save_objects(records)
        db.flush()
        logger.info("Seeded %d service records", len(records))

    # ------------------------------------------------------------------ #
    # Service Requests                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_service_requests(db: Session) -> None:
        requests = [
            # THE DEMO TRIGGER — EQUIP-001 HVAC-204 open request
            ServiceRequest(
                id="SR-1042",
                title="Cooling System Failure - HVAC-204",
                reported_symptoms=(
                    "Cooling performance has dropped significantly. Building temperature cannot be maintained. "
                    "Staff reporting discomfort. Issue escalated by site manager. "
                    "This is the fourth time this unit has had cooling issues this year."
                ),
                equipment_id="EQUIP-001",
                site_id="SITE-001",
                customer_id="CUST-001",
                technician_id="TECH-005",
                priority="High",
                status="Assigned",
                is_demo_trigger=True,
            ),
            # Other open requests
            ServiceRequest(
                id="SR-1043",
                title="Boiler BLRM-Steel-01 Pressure Instability",
                reported_symptoms="Recurring pressure fluctuations. Operators requesting urgent inspection.",
                equipment_id="EQUIP-016",
                site_id="SITE-005",
                customer_id="CUST-004",
                technician_id="TECH-007",
                priority="High",
                status="Assigned",
                is_demo_trigger=False,
            ),
            ServiceRequest(
                id="SR-1044",
                title="COMP-Delhi-01 Temperature Alarm Recurring",
                reported_symptoms="Screw element temperature alarm again. Unit tripped.",
                equipment_id="EQUIP-029",
                site_id="SITE-003",
                customer_id="CUST-002",
                technician_id="TECH-002",
                priority="Medium",
                status="Open",
                is_demo_trigger=False,
            ),
            ServiceRequest(
                id="SR-1040",
                title="Resolved: CT-REF-01 Scaling — Dosing Pump Replaced",
                reported_symptoms="Cooling tower approach temperature elevated.",
                equipment_id="EQUIP-022",
                site_id="SITE-004",
                customer_id="CUST-003",
                technician_id="TECH-010",
                priority="Medium",
                status="Resolved",
                is_demo_trigger=False,
            ),
            ServiceRequest(
                id="SR-1041",
                title="Resolved: HYD-PRESS-02 Pressure Drop",
                reported_symptoms="Hydraulic press not reaching full tonnage.",
                equipment_id="EQUIP-020",
                site_id="SITE-008",
                customer_id="CUST-007",
                technician_id="TECH-009",
                priority="High",
                status="Resolved",
                is_demo_trigger=False,
            ),
        ]
        db.bulk_save_objects(requests)
        db.flush()
        logger.info("Seeded %d service requests", len(requests))

    # ------------------------------------------------------------------ #
    # Memory Items (30+)                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _seed_memory_items(db: Session) -> None:  # noqa: C901
        now_iso = datetime.utcnow().isoformat()

        items = [
            # ============================================================
            # EQUIP-001 (HVAC-204) memories
            # ============================================================
            MemoryItem(
                id="MEM-001",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-001",
                entity_name="HVAC-204",
                title="HVAC-204: Filter + Coil Clean Fixed Cooling Drop (Apr 2025)",
                content=(
                    "SERVICE VISIT — HVAC-204 (HVAC)\n"
                    "Date: 2025-04-10\nTechnician: Ravi Shankar\n"
                    "Site: Hyderabad Plant | Customer: ABC Manufacturing Co.\n\n"
                    "SYMPTOMS OBSERVED: Cooling performance dropped 40%. Unit struggling to maintain setpoint of 22°C.\n"
                    "ACTION TAKEN: Replaced dirty air filters. Cleaned condenser coils. Topped up refrigerant by 200g.\n"
                    "PARTS REPLACED: Air filters x4\n"
                    "OUTCOME: Resolved\n"
                    "EFFECTIVE DURATION: 45 days before recurrence\n"
                    "TECHNICIAN NOTES: Unit had heavily clogged filters. Compressor rattle at startup heard — worth monitoring."
                ),
                context="Site: Hyderabad Plant | Customer: ABC Manufacturing Co. | Equipment: HVAC-204 (HVAC) | Visit #1",
                source_incident_id="SREC-001",
                source_technician_name="Ravi Shankar",
                tags="EQUIP-001,SITE-001,CUST-001,hvac,filter_replacement",
                timestamp="2025-04-10",
                confidence=0.95,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),
            MemoryItem(
                id="MEM-002",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-001",
                entity_name="HVAC-204",
                title="HVAC-204: TXV Valve Replacement Gave Only 38-Day Relief (May 2025)",
                content=(
                    "SERVICE VISIT — HVAC-204 (HVAC)\n"
                    "Date: 2025-05-25\nTechnician: Deepa Nayak\n"
                    "Site: Hyderabad Plant | Customer: ABC Manufacturing Co.\n\n"
                    "SYMPTOMS OBSERVED: Cooling performance degraded again. Noise from compressor section.\n"
                    "ACTION TAKEN: Replaced TXV valve that was partially stuck. Adjusted refrigerant charge.\n"
                    "PARTS REPLACED: TXV Valve\n"
                    "OUTCOME: Temporarily Resolved\n"
                    "EFFECTIVE DURATION: 38 days before recurrence\n"
                    "TECHNICIAN NOTES: Compressor vibration 4.2 mm/s — above 3.5 alarm. Client should plan compressor overhaul. "
                    "High ambient temperature (38°C) in equipment room accelerating degradation."
                ),
                context="Site: Hyderabad Plant | Customer: ABC Manufacturing Co. | Equipment: HVAC-204 (HVAC) | Visit #2",
                source_incident_id="SREC-002",
                source_technician_name="Deepa Nayak",
                tags="EQUIP-001,SITE-001,CUST-001,hvac,txv_valve,compressor_wear",
                timestamp="2025-05-25",
                confidence=0.97,
                recurrence_flag=True,
                outcome_status="Temporarily Resolved",
            ),
            MemoryItem(
                id="MEM-003",
                bank_id="field-service-org-memory",
                memory_type="EQUIPMENT_RECURRENCE",
                entity_type="equipment",
                entity_id="EQUIP-001",
                entity_name="HVAC-204",
                title="HVAC-204: Third Visit — Refrigerant Leak + Compressor Critical (Jul 2025)",
                content=(
                    "SERVICE VISIT — HVAC-204 (HVAC)\n"
                    "Date: 2025-07-02\nTechnician: Ravi Shankar\n"
                    "Site: Hyderabad Plant | Customer: ABC Manufacturing Co.\n\n"
                    "SYMPTOMS OBSERVED: Unit completely failed to cool. Compressor tripping on high pressure fault.\n"
                    "ACTION TAKEN: Repaired refrigerant leak. Re-pressurized system. Reset high pressure fault.\n"
                    "PARTS REPLACED: Copper pipe joint, Schrader valve\n"
                    "OUTCOME: Temporarily Resolved\n"
                    "TECHNICIAN NOTES: Third visit for similar issues. Root cause is ageing compressor. "
                    "Compressor vibration 6.1 mm/s vs 2.5 baseline — CRITICAL. Strongly recommend compressor replacement. "
                    "Risk: if compressor fails, 2-3 weeks without cooling (lead time)."
                ),
                context="Site: Hyderabad Plant | Customer: ABC Manufacturing Co. | Equipment: HVAC-204 (HVAC) | Visit #3",
                source_incident_id="SREC-003",
                source_technician_name="Ravi Shankar",
                tags="EQUIP-001,SITE-001,CUST-001,hvac,refrigerant_leak,compressor_failure,recurrence",
                timestamp="2025-07-02",
                confidence=0.99,
                recurrence_flag=True,
                outcome_status="Temporarily Resolved",
            ),
            MemoryItem(
                id="MEM-004",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-001",
                entity_name="HVAC-204",
                title="HVAC-204: Compressor Bearing Wear Confirmed — Replacement Urgently Needed",
                content=(
                    "CRITICAL OBSERVATION: HVAC-204 compressor bearing wear confirmed across 3 visits (Apr–Jul 2025). "
                    "Vibration progression: Visit 1 (Apr): slight rattle noted | "
                    "Visit 2 (May): 4.2 mm/s RMS — above 3.5 alarm | "
                    "Visit 3 (Jul): 6.1 mm/s RMS — CRITICAL, 140% above baseline. "
                    "Each symptom-treatment fix has been temporary (45 days, 38 days). "
                    "Root cause is NOT being addressed. COMPRESSOR REPLACEMENT IS THE ONLY PERMANENT FIX. "
                    "Equipment room ambient temperature 38°C is also a contributing factor — ventilation improvement needed."
                ),
                context="Cross-visit pattern analysis | HVAC-204 | Hyderabad Plant",
                source_incident_id="SREC-003",
                source_technician_name="Ravi Shankar",
                tags="EQUIP-001,SITE-001,compressor_wear,critical_pattern,bearing_failure",
                timestamp="2025-07-02",
                confidence=0.99,
                recurrence_flag=True,
                outcome_status="Requires Escalation",
            ),
            MemoryItem(
                id="MEM-005",
                bank_id="field-service-org-memory",
                memory_type="SITE_ENVIRONMENTAL",
                entity_type="site",
                entity_id="SITE-001",
                entity_name="Hyderabad Plant",
                title="Hyderabad Plant: Equipment Room Overheating — Poor Ventilation",
                content=(
                    "SITE ENVIRONMENTAL NOTE: Equipment room at Hyderabad Plant consistently at 38°C ambient "
                    "during summer months. Rated maximum operating ambient for HVAC-204 is 35°C. "
                    "This excess heat is accelerating compressor degradation across all HVAC units at this site. "
                    "Recommendation: Install exhaust ventilation fan in equipment room. "
                    "This was noted by both Ravi Shankar (Apr 2025) and Deepa Nayak (May 2025)."
                ),
                context="Site: Hyderabad Plant | Multiple technician observations",
                source_incident_id="SREC-002",
                source_technician_name="Deepa Nayak",
                tags="SITE-001,CUST-001,environmental,high_ambient,ventilation",
                timestamp="2025-05-25",
                confidence=0.93,
                recurrence_flag=False,
                outcome_status="",
            ),

            # ============================================================
            # EQUIP-002 (CWP-12) memories
            # ============================================================
            MemoryItem(
                id="MEM-006",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-002",
                entity_name="CWP-12",
                title="CWP-12: Impeller + Bearing Replacement — Cavitation Pattern Recurring",
                content=(
                    "SERVICE VISIT — CWP-12 (Industrial Pump)\n"
                    "Date: 2025-02-14\nTechnician: Mohammed Al-Farsi\n"
                    "Classic cavitation damage. Impeller replaced. Issue returned in 90 days. "
                    "Root cause: inlet strainer blocking from upstream pipeline debris. "
                    "Auto self-cleaning strainer recommended."
                ),
                source_incident_id="SREC-004",
                source_technician_name="Mohammed Al-Farsi",
                tags="EQUIP-002,SITE-004,cavitation,pump,impeller,strainer",
                timestamp="2025-02-14",
                confidence=0.96,
                recurrence_flag=True,
                outcome_status="Resolved",
            ),
            MemoryItem(
                id="MEM-007",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-002",
                entity_name="CWP-12",
                title="CWP-12: Second Cavitation Incident — Upstream Pipeline Root Cause",
                content=(
                    "Second cavitation incident in 3 months on CWP-12. Bearing replaced again. "
                    "Root cause: debris from deteriorating upstream pipeline repeatedly blocking inlet strainer. "
                    "Recommend: (1) Pipeline inspection and possible relining. "
                    "(2) Upgrade to self-cleaning strainer. "
                    "(3) Consider duplex pump arrangement — this is a single point of failure."
                ),
                source_incident_id="SREC-005",
                source_technician_name="Mohammed Al-Farsi",
                tags="EQUIP-002,SITE-004,cavitation,bearing,pipeline_deterioration",
                timestamp="2025-05-15",
                confidence=0.98,
                recurrence_flag=True,
                outcome_status="Temporarily Resolved",
            ),
            MemoryItem(
                id="MEM-008",
                bank_id="field-service-org-memory",
                memory_type="EQUIPMENT_RECURRENCE",
                entity_type="equipment",
                entity_id="EQUIP-002",
                entity_name="CWP-12",
                title="CWP-12: Complete Failure — Third Incident, Emergency Repair",
                content=(
                    "CWP-12 completely failed — impeller corroded through, shaft seal failed. "
                    "Third major intervention in 6 months. Emergency repair performed. "
                    "STRONG RECOMMENDATION: Install duplex pump (N+1 redundancy). "
                    "Current single-pump design is a single point of failure for refinery cooling circuit."
                ),
                source_incident_id="SREC-006",
                source_technician_name="Kiran Patel",
                tags="EQUIP-002,SITE-004,pump_failure,duplex_recommendation,critical",
                timestamp="2025-07-20",
                confidence=0.99,
                recurrence_flag=True,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-004 (COMP-A3) memories
            # ============================================================
            MemoryItem(
                id="MEM-009",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-004",
                entity_name="COMP-A3",
                title="COMP-A3: Bearing Failure — Oil Cooler Fouling Root Cause",
                content=(
                    "Multiple bearing failures on COMP-A3. Root cause identified: oil cooler fouled by blast furnace dust "
                    "→ high oil temperature (92°C vs 70°C normal) → lubricant degradation → premature bearing failure. "
                    "Full overhaul in Feb 2025 included upgraded oil cooler with better dust exclusion. "
                    "LESSON: In dusty/industrial environments, oil cooler cleaning is as important as bearing replacement."
                ),
                source_incident_id="SREC-009",
                source_technician_name="Anjali Krishnan",
                tags="EQUIP-004,SITE-005,compressor,bearing,oil_cooler,dust,root_cause",
                timestamp="2025-02-28",
                confidence=0.99,
                recurrence_flag=True,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-005 (BLRM-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-010",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-005",
                entity_name="BLRM-01",
                title="BLRM-01: SRV Drift — Replace Annually per BS EN 4126",
                content=(
                    "Safety Relief Valve on BLRM-01 drifted low (lifting at 9.8 bar vs 10.5 bar setpoint). "
                    "Caused by seat corrosion in steam environment. Replace SRV every 12 months. "
                    "Combustion efficiency issue (79%) resolved by cleaning economiser. "
                    "Annual maintenance: descale economiser, check O2 sensor, test SRV."
                ),
                source_incident_id="SREC-010",
                source_technician_name="Arjun Bhat",
                tags="EQUIP-005,SITE-007,boiler,srv,safety_valve,economiser",
                timestamp="2025-01-20",
                confidence=0.95,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-016 (BLRM-Steel-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-011",
                bank_id="field-service-org-memory",
                memory_type="EQUIPMENT_RECURRENCE",
                entity_type="equipment",
                entity_id="EQUIP-016",
                entity_name="BLRM-Steel-01",
                title="BLRM-Steel-01: Ageing Boiler — Multiple System Failures, Replacement Recommended",
                content=(
                    "BLRM-Steel-01 (9 years old) showing multiple concurrent failure modes: "
                    "scale buildup (Jan 2025), burner lockout (Mar 2025, May 2025). "
                    "Pattern typical of end-of-life equipment. "
                    "Statutory vessel inspection due. Tube wall thickness check needed. "
                    "RECOMMENDATION: Plan boiler replacement in next capital budget cycle."
                ),
                source_incident_id="SREC-025",
                source_technician_name="Arjun Bhat",
                tags="EQUIP-016,SITE-005,boiler,ageing,end_of_life,replacement",
                timestamp="2025-05-01",
                confidence=0.97,
                recurrence_flag=True,
                outcome_status="Temporarily Resolved",
            ),

            # ============================================================
            # EQUIP-022 (CT-REF-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-012",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-022",
                entity_name="CT-REF-01",
                title="CT-REF-01: Cooling Tower Scaling — Dosing Pump Failure Caused Rapid Recurrence",
                content=(
                    "Severe calcium carbonate scaling on CT-REF-01. Original treatment: acid descale + fill media replacement. "
                    "Recurrence in 3 months due to dosing pump failure (3-week gap in biocide). "
                    "ROOT CAUSE PATTERN: Chemical treatment infrastructure must be redundant. "
                    "RECOMMENDATION: Install redundant dosing pump with alarm if primary fails. "
                    "Water softener or online dosing monitor also recommended for high-hardness make-up water."
                ),
                source_incident_id="SREC-013",
                source_technician_name="Asha Bhatt",
                tags="EQUIP-022,SITE-004,cooling_tower,scaling,dosing_pump,redundancy",
                timestamp="2025-06-15",
                confidence=0.96,
                recurrence_flag=True,
                outcome_status="Temporarily Resolved",
            ),

            # ============================================================
            # EQUIP-020 (HYD-PRESS-02) memories
            # ============================================================
            MemoryItem(
                id="MEM-013",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-020",
                entity_name="HYD-PRESS-02",
                title="HYD-PRESS-02: Hydraulic Contamination Root Cause — Cylinder Seal Failure",
                content=(
                    "HYD-PRESS-02 pressure issues resolved after cylinder seal replacement and bore honing. "
                    "Root cause: cylinder seal failure → particulate contamination of hydraulic fluid → "
                    "pump wear → loss of pressure. "
                    "LESSON: Hydraulic fluid contamination is often a symptom, not a root cause. "
                    "Trace contamination source before simply changing fluid."
                ),
                source_incident_id="SREC-015",
                source_technician_name="Kiran Patel",
                tags="EQUIP-020,SITE-008,hydraulic,cylinder_seal,contamination,root_cause",
                timestamp="2025-06-10",
                confidence=0.97,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-010 (FWP-03) memories
            # ============================================================
            MemoryItem(
                id="MEM-014",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-010",
                entity_name="FWP-03",
                title="FWP-03: Standard Seal Incompatible With High-Temp Process — Upgraded to PTFE",
                content=(
                    "FWP-03 shaft seal failed after only 4 months — standard material incompatible with 80°C+ process fluid. "
                    "Upgraded to high-temperature PTFE seal (rated to 120°C). "
                    "LESSON: Always verify seal material compatibility with maximum process temperature. "
                    "Standard NBR seals degrade rapidly above 80°C. PTFE or EPDM required for high-temperature service."
                ),
                source_incident_id="SREC-045",
                source_technician_name="Mohammed Al-Farsi",
                tags="EQUIP-010,SITE-005,pump,shaft_seal,high_temperature,ptfe,material_selection",
                timestamp="2025-07-05",
                confidence=0.97,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-025 (GEN-BACKUP-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-015",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-025",
                entity_name="GEN-BACKUP-01",
                title="GEN-BACKUP-01: Starter Battery Failure — Replace Every 3 Years",
                content=(
                    "Hospital backup generator failed auto-start due to 5-year-old starter batteries (minimum 24V not met). "
                    "Batteries replaced — auto-transfer now working correctly. "
                    "LESSON: Standby generators must have batteries on fixed replacement schedule — not condition-monitored. "
                    "Industry best practice: replace every 3 years regardless of apparent condition."
                ),
                source_incident_id="SREC-019",
                source_technician_name="Priyanka Joshi",
                tags="EQUIP-025,SITE-009,generator,battery,hospital,critical,replacement_interval",
                timestamp="2025-04-05",
                confidence=0.99,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-017 (TRB-GEN-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-016",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-017",
                entity_name="TRB-GEN-01",
                title="TRB-GEN-01: Rotor Unbalance — Annual Trim Balance Required",
                content=(
                    "TRB-GEN-01 vibration increased to 85 µm due to rotor unbalance (blade erosion over time). "
                    "Trim balance correction applied — vibration reduced to 42 µm. "
                    "PATTERN: Annual trim balance is routine maintenance for this turbine. "
                    "Schedule next balance in February 2026."
                ),
                source_incident_id="SREC-018",
                source_technician_name="Anjali Krishnan",
                tags="EQUIP-017,SITE-007,turbine,vibration,balance,rotor,maintenance_interval",
                timestamp="2025-02-10",
                confidence=0.94,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-006 (HVAC-115 ICU) memories
            # ============================================================
            MemoryItem(
                id="MEM-017",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-006",
                entity_name="HVAC-115",
                title="HVAC-115 ICU: Condenser Bearing Life ~28,000 Hours — Proactive Policy",
                content=(
                    "ICU HVAC-115 condenser fan bearings failed at 28,000+ operating hours (5 years). "
                    "Backup HVAC-116 activated for 4 hours during repair. "
                    "POLICY RECOMMENDATION for critical healthcare HVAC: replace condenser bearings proactively at "
                    "25,000 hours (~4.5 years) to prevent unplanned failures in a live ICU environment. "
                    "Also: check HVAC-116 backup unit bearings proactively."
                ),
                source_incident_id="SREC-016",
                source_technician_name="Deepa Nayak",
                tags="EQUIP-006,SITE-009,hvac,hospital,icu,bearing,proactive_maintenance,critical",
                timestamp="2025-03-12",
                confidence=0.96,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-024 (CT-Power-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-018",
                bank_id="field-service-org-memory",
                memory_type="EQUIPMENT_RECURRENCE",
                entity_type="equipment",
                entity_id="EQUIP-024",
                entity_name="CT-Power-01",
                title="CT-Power-01: Fan Gearbox End of Life — Failed Earlier Than Predicted",
                content=(
                    "10-year-old cooling tower gearbox failed unexpectedly after only 90 days of temporary operation. "
                    "Turbine derated to 60% during emergency gearbox replacement. "
                    "LESSON: Once micropitting is observed on gear teeth and iron content exceeds 200 ppm in oil, "
                    "remaining life is unpredictable. Do not defer replacement beyond one planned outage."
                ),
                source_incident_id="SREC-032",
                source_technician_name="Asha Bhatt",
                tags="EQUIP-024,SITE-007,cooling_tower,gearbox,failure,power_generation",
                timestamp="2025-07-15",
                confidence=0.98,
                recurrence_flag=True,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-027 (GEN-Infosys-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-019",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-027",
                entity_name="GEN-Infosys-01",
                title="GEN-Infosys-01: Exciter Diode Bridge Failure — Known Failure Mode at 6+ Years",
                content=(
                    "Generator AVR instability caused by failed exciter diode bridge. "
                    "This is a known failure mode for this generator model after 6+ years of service. "
                    "STOCK RECOMMENDATION: Keep spare exciter diode bridge in inventory — lead time is 3 weeks. "
                    "Monitor for voltage instability during monthly load tests."
                ),
                source_incident_id="SREC-033",
                source_technician_name="Priyanka Joshi",
                tags="EQUIP-027,SITE-006,generator,avr,diode,exciter,spare_parts",
                timestamp="2025-06-20",
                confidence=0.93,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-013 (COMP-Refinery-02) memories
            # ============================================================
            MemoryItem(
                id="MEM-020",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-013",
                entity_name="COMP-Refinery-02",
                title="COMP-Refinery-02: Inlet Valve Overhaul at 63,000h — All Stages",
                content=(
                    "Stage 2 inlet valve spring fatigue at 63,000 hours. "
                    "Proactively replaced valve plates on all stages — prevents future unplanned outages. "
                    "BEST PRACTICE: When opening for one stage valve, replace all stages simultaneously. "
                    "Valve spring fatigue is normal at 60,000+ hours for this compressor design."
                ),
                source_incident_id="SREC-023",
                source_technician_name="Anjali Krishnan",
                tags="EQUIP-013,SITE-004,compressor,valve,overhaul,preventive",
                timestamp="2024-10-15",
                confidence=0.94,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-011 (CWP-Hazira-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-021",
                bank_id="field-service-org-memory",
                memory_type="SUCCESSFUL_FIX",
                entity_type="equipment",
                entity_id="EQUIP-011",
                entity_name="CWP-Hazira-01",
                title="CWP-Hazira-01: Seawater Pump — Duplex SS Impeller Upgrade for Corrosion Resistance",
                content=(
                    "Seawater pump impeller severely corroded — lost 15mm from blade tips. "
                    "Upgraded to duplex stainless steel impeller for better corrosion resistance. "
                    "RECOMMENDATION: Apply sacrificial anodes to pump casing for cathodic protection. "
                    "In seawater service, material selection is critical — standard SS corrodes rapidly."
                ),
                source_incident_id="SREC-029",
                source_technician_name="Mohammed Al-Farsi",
                tags="EQUIP-011,SITE-010,pump,seawater,corrosion,duplex_ss,material_upgrade",
                timestamp="2025-06-01",
                confidence=0.96,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),

            # ============================================================
            # EQUIP-009 (HVAC-Chennai-01) memories
            # ============================================================
            MemoryItem(
                id="MEM-022",
                bank_id="field-service-org-memory",
                memory_type="FAILED_FIX",
                entity_type="equipment",
                entity_id="EQUIP-009",
                entity_name="HVAC-Chennai-01",
                title="HVAC-Chennai-01: High Ambient Temp Exceeds Unit Design — Temporary Shade Fix",
                content=(
                    "HVAC-Chennai-01 repeatedly trips on high pressure when ambient exceeds 40°C. "
                    "Shade structure installed — but removed by site team during maintenance, causing recurrence. "
                    "PERMANENT FIX OPTIONS: (1) Condenser fan boosters to increase airflow. "
                    "(2) Relocate condenser to shaded area. (3) Upgrade to unit rated for 45°C ambient. "
                    "Current unit designed for max 40°C — Chennai summers regularly exceed this."
                ),
                source_incident_id="SREC-022",
                source_technician_name="Vikram Malhotra",
                tags="EQUIP-009,SITE-012,hvac,high_ambient,design_limit,shade,temporary_fix",
                timestamp="2025-06-08",
                confidence=0.95,
                recurrence_flag=True,
                outcome_status="Resolved",
            ),

            # ============================================================
            # Site-level memories
            # ============================================================
            MemoryItem(
                id="MEM-023",
                bank_id="field-service-org-memory",
                memory_type="SITE_ENVIRONMENTAL",
                entity_type="site",
                entity_id="SITE-004",
                entity_name="Jamnagar Refinery",
                title="Jamnagar Refinery: High Water Hardness — Scaling Affects All Cooling Equipment",
                content=(
                    "Jamnagar Refinery make-up water hardness consistently 600-850 ppm (target <300 ppm). "
                    "This causes scaling in all cooling systems: CT-REF-01 and CWP-12 both affected. "
                    "SITE-WIDE RECOMMENDATION: Install centralised water softening plant for cooling water supply. "
                    "Current chemical dosing is fighting a losing battle against naturally hard source water."
                ),
                source_incident_id="SREC-012",
                source_technician_name="Mohammed Al-Farsi",
                tags="SITE-004,CUST-003,water_quality,hardness,scaling,site_wide_issue",
                timestamp="2025-03-05",
                confidence=0.95,
                recurrence_flag=True,
                outcome_status="",
            ),
            MemoryItem(
                id="MEM-024",
                bank_id="field-service-org-memory",
                memory_type="SITE_ENVIRONMENTAL",
                entity_type="site",
                entity_id="SITE-005",
                entity_name="Blast Furnace Block A",
                title="Blast Furnace Block A: Extreme Dust — Oil Cooling Systems Must Be Enclosed",
                content=(
                    "Blast furnace dust ingress into compressor (COMP-A3) oil cooling system caused multiple bearing failures. "
                    "Dust particle size 50-200 µm — highly abrasive. "
                    "ALL oil cooling systems at this site should have enclosed/filtered air intake. "
                    "Oil analysis every 1000 hours mandatory — iron content >50 ppm should trigger immediate inspection."
                ),
                source_incident_id="SREC-009",
                source_technician_name="Anjali Krishnan",
                tags="SITE-005,CUST-004,dust,oil_contamination,compressor,bearing,site_wide",
                timestamp="2025-02-28",
                confidence=0.97,
                recurrence_flag=False,
                outcome_status="",
            ),
            MemoryItem(
                id="MEM-025",
                bank_id="field-service-org-memory",
                memory_type="SITE_ENVIRONMENTAL",
                entity_type="site",
                entity_id="SITE-003",
                entity_name="Blue Line Depot",
                title="Blue Line Depot: Metro Tunnel Dust Blocks Oil Cooler Fins Every 3-4 Months",
                content=(
                    "Metro tunnel environment generates significant fine dust from rail and brake wear. "
                    "COMP-Delhi-01 oil cooler fins block every 3-4 months — accelerated vs typical 12-month interval. "
                    "SOLUTION: Add foam pre-filter to compressor cooler air intake. "
                    "Thermostatic bypass valve also failed — stock spare recommended."
                ),
                source_incident_id="SREC-034",
                source_technician_name="Priyanka Joshi",
                tags="SITE-003,CUST-002,tunnel_dust,compressor,oil_cooler,maintenance_interval",
                timestamp="2025-06-30",
                confidence=0.93,
                recurrence_flag=False,
                outcome_status="",
            ),

            # ============================================================
            # Customer-level memories
            # ============================================================
            MemoryItem(
                id="MEM-026",
                bank_id="field-service-org-memory",
                memory_type="CUSTOMER_PREFERENCE",
                entity_type="customer",
                entity_id="CUST-003",
                entity_name="Reliance Petrochemicals",
                title="Reliance Petrochemicals: ATEX Certification and Permit-to-Work Mandatory",
                content=(
                    "ALL field engineers visiting Reliance Petrochemicals sites must: "
                    "(1) Hold valid ATEX certification for Zone 1 hazardous areas. "
                    "(2) Obtain Permit-to-Work before any activity. "
                    "(3) Use ATEX-rated tools and instruments only. "
                    "(4) Complete hot work permit for any brazing or welding. "
                    "Site security checks documentation at gate — non-compliance means site rejection."
                ),
                source_incident_id=None,
                source_technician_name="Mohammed Al-Farsi",
                tags="CUST-003,SITE-004,SITE-010,atex,permit_to_work,safety,compliance",
                timestamp="2025-01-01",
                confidence=1.0,
                recurrence_flag=False,
                outcome_status="",
            ),
            MemoryItem(
                id="MEM-027",
                bank_id="field-service-org-memory",
                memory_type="CUSTOMER_PREFERENCE",
                entity_type="customer",
                entity_id="CUST-008",
                entity_name="Apollo Hospitals Chennai",
                title="Apollo Hospitals: ICU Work Requires Infection Control Protocol + Silent Tools",
                content=(
                    "ICU HVAC work at Apollo Hospitals requires: "
                    "(1) Full infection control: sterile gloves, mask, overshoes. "
                    "(2) All work outside patient hours (before 6AM or after 10PM). "
                    "(3) No power tools that generate significant noise or vibration near patient areas. "
                    "(4) Any unplanned failure triggers immediate escalation to site facilities manager. "
                    "Contact: Dr. Arun Bose (+91-44-89012345). SLA: 4-hour response for ICU equipment."
                ),
                source_incident_id=None,
                source_technician_name="Deepa Nayak",
                tags="CUST-008,SITE-009,hospital,icu,infection_control,sla,protocol",
                timestamp="2025-01-01",
                confidence=1.0,
                recurrence_flag=False,
                outcome_status="",
            ),
            MemoryItem(
                id="MEM-028",
                bank_id="field-service-org-memory",
                memory_type="CUSTOMER_PREFERENCE",
                entity_type="customer",
                entity_id="CUST-004",
                entity_name="Tata Steel Jamshedpur",
                title="Tata Steel: Heat-Resistant PPE Required — Ambient 45°C+ Near Furnaces",
                content=(
                    "Tata Steel Jamshedpur Blast Furnace area: ambient temperature regularly 45°C+. "
                    "MANDATORY PPE: Aluminised heat-resistant suit, face shield, insulated gloves. "
                    "Buddy system: no lone working. Max 30 minutes near furnace before rotation. "
                    "All equipment and instruments must be rated for operation in high-heat environments."
                ),
                source_incident_id=None,
                source_technician_name="Anjali Krishnan",
                tags="CUST-004,SITE-005,heat,ppe,safety,extreme_environment",
                timestamp="2025-01-01",
                confidence=1.0,
                recurrence_flag=False,
                outcome_status="",
            ),

            # ============================================================
            # Cross-cutting / analytical memories
            # ============================================================
            MemoryItem(
                id="MEM-029",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-003",
                entity_name="AHU-07",
                title="AHU-07: Proactive Bearing Replacement at 3.2mm/s Prevented Failure",
                content=(
                    "AHU-07 fan bearings showing early wear (3.2 mm/s — alert threshold 3.5 mm/s). "
                    "Proactive replacement performed — avoided certain failure in 2-3 months. "
                    "LESSON: Vibration monitoring enables planned replacement vs emergency breakdown. "
                    "Recommend installing permanent vibration monitoring on all critical HVAC units."
                ),
                source_incident_id="SREC-027",
                source_technician_name="Deepa Nayak",
                tags="EQUIP-003,SITE-006,hvac,bearing,proactive_maintenance,vibration_monitoring",
                timestamp="2025-08-18",
                confidence=0.92,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),
            MemoryItem(
                id="MEM-030",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-029",
                entity_name="COMP-Delhi-01",
                title="COMP-Delhi-01: Foam Pre-Filter on Cooler Inlet Will Reduce Blockage Frequency",
                content=(
                    "Metro tunnel dust causing oil cooler fin blockage every 3-4 months on COMP-Delhi-01. "
                    "Recommended solution: add foam pre-filter on cooler air intake. "
                    "Low-cost modification expected to extend cleaning interval to 9-12 months. "
                    "Thermostatic bypass valve replacement also needed — failure caused overheating."
                ),
                source_incident_id="SREC-034",
                source_technician_name="Priyanka Joshi",
                tags="EQUIP-029,SITE-003,compressor,dust,foam_filter,modification",
                timestamp="2025-06-30",
                confidence=0.91,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),
            MemoryItem(
                id="MEM-031",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-019",
                entity_name="HYD-PRESS-01",
                title="HYD-PRESS-01: Normal Seal Wear at 40,000h — Scheduled Replacement Effective",
                content=(
                    "HYD-PRESS-01 gland seal replaced at 40,000+ hours — normal wear. "
                    "Scheduled replacement during planned downtime — no unplanned production loss. "
                    "BEST PRACTICE: Hydraulic press seals should be on fixed replacement schedule "
                    "(typically every 2-3 years or per operating hours per OEM recommendation)."
                ),
                source_incident_id="SREC-030",
                source_technician_name="Kiran Patel",
                tags="EQUIP-019,SITE-008,hydraulic,seal,scheduled_maintenance",
                timestamp="2025-04-01",
                confidence=0.90,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),
            MemoryItem(
                id="MEM-032",
                bank_id="field-service-org-memory",
                memory_type="TECHNICIAN_OBSERVATION",
                entity_type="equipment",
                entity_id="EQUIP-002",
                entity_name="CWP-12",
                title="CWP-12: Remote Vibration Monitoring Installed — Customer Sensitised After 3 Failures",
                content=(
                    "After 3 major pump failures in 6 months, customer sensitised to any CWP-12 noise. "
                    "Remote vibration monitoring set up to provide objective data. "
                    "Initial post-repair check: 2.1 mm/s — excellent. Unit is healthy. "
                    "Monitoring will alert before next failure event — expected to build customer confidence."
                ),
                source_incident_id="SREC-052",
                source_technician_name="Mohammed Al-Farsi",
                tags="EQUIP-002,SITE-004,pump,remote_monitoring,vibration,customer_confidence",
                timestamp="2025-08-15",
                confidence=0.88,
                recurrence_flag=False,
                outcome_status="Resolved",
            ),
        ]

        db.bulk_save_objects(items)
        db.flush()
        logger.info("Seeded %d memory items", len(items))
