#!/usr/bin/python3
import random
from datetime import date, timedelta
import threading
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from collections import defaultdict
import random

World_fleet = {
    "merchant_fleet_breakdown": {
        "bulk_carrier": {
            "count": 13141,
            "average_age": 11.7
        },
        "container_ship": {
            "count": 5815,
            "average_age": 14.1
        },
        "general_cargo": {
            "count": 19918,
            "average_age": 26.4
        },
        "oil_tanker": {
            "count": 11604,
            "average_age": 12.8
        },
        "other_vessels": {
            "count": 53099,
            "average_age": 22.5
        }
    },

    "other_vessel_types": {
        "tugboats": {
            "count": 17200,
            "average_age": 24.3
        },
        "fishing_vessels_large": {
            "count": 65000,
            "average_age": 28.0
        },
        "cruise_ships": {
            "count": 400,
            "average_age": 22.6
        },
        "lng_carriers": {
            "count": 700,
            "average_age": 10.1
        },
        "lpg_carriers": {
            "count": 1500,
            "average_age": 13.5
        },
        "offshore_support_vessels": {
            "count": 6000,
            "average_age": 17.8
        },
        "research_vessels": {
            "count": 600,
            "average_age": 25.0
        },
        "ro_ro_ships": {
            "count": 1300,
            "average_age": 19.6
        }
    },

    "naval_forces_by_country": {
        "China": {"count": 777, "average_age": 10},
        "United States": {"count": 490, "average_age": 14},
        "Russia": {"count": 603, "average_age": 20},
        "Indonesia": {"count": 282, "average_age": 25},
        "India": {"count": 285, "average_age": 18},
        "Thailand": {"count": 292, "average_age": 20},
        "Iran": {"count": 398, "average_age": 22},
        "Colombia": {"count": 453, "average_age": 18},
        "Egypt": {"count": 316, "average_age": 20},
        "North Korea": {"count": 492, "average_age": 28},
        "Sri Lanka": {"count": 270, "average_age": 22},
        "Sweden": {"count": 308, "average_age": 15},
        "Finland": {"count": 264, "average_age": 15},
        "South Korea": {"count": 227, "average_age": 12},
        "Myanmar": {"count": 232, "average_age": 30},
        "Italy": {"count": 196, "average_age": 17},
        "Portugal": {"count": 194, "average_age": 22},
        "Japan": {"count": 155, "average_age": 13},
        "France": {"count": 110, "average_age": 15},
        "United Kingdom": {"count": 60, "average_age": 14},
        "Turkey": {"count": 90, "average_age": 18},
        "Australia": {"count": 48, "average_age": 15},
        "Canada": {"count": 35, "average_age": 16},
        "Germany": {"count": 65, "average_age": 14},
        "Brazil": {"count": 99, "average_age": 20},
        "Mexico": {"count": 72, "average_age": 25},
        "Argentina": {"count": 45, "average_age": 30},
        "Netherlands": {"count": 32, "average_age": 13},
        "Norway": {"count": 30, "average_age": 12},
        "Greece": {"count": 35, "average_age": 20},
        "Spain": {"count": 42, "average_age": 15},
        "South Africa": {"count": 22, "average_age": 25},
        "New Zealand": {"count": 11, "average_age": 18},
        "Philippines": {"count": 41, "average_age": 22},
        "Vietnam": {"count": 63, "average_age": 20},
        "Bangladesh": {"count": 42, "average_age": 20},
        "Chile": {"count": 46, "average_age": 18},
        "Singapore": {"count": 25, "average_age": 10},
        "Malaysia": {"count": 40, "average_age": 15},
        "Israel": {"count": 69, "average_age": 15},
        "Pakistan": {"count": 45, "average_age": 22},
        "Algeria": {"count": 70, "average_age": 25},
        "Saudi Arabia": {"count": 65, "average_age": 18},
        "United Arab Emirates": {"count": 50, "average_age": 12},
        "Qatar": {"count": 15, "average_age": 10},
        "Kuwait": {"count": 25, "average_age": 15},
        "Lebanon": {"count": 10, "average_age": 25},
        "Jordan": {"count": 3, "average_age": 30},
        "Iceland": {"count": 4, "average_age": 20},
        "Ireland": {"count": 5, "average_age": 18},
        "Fiji": {"count": 3, "average_age": 25},
        "Papua New Guinea": {"count": 4, "average_age": 25},
        "Malta": {"count": 2, "average_age": 30},
        "Bahamas": {"count": 1, "average_age": 35},
        "Barbados": {"count": 1, "average_age": 30},
        "Mauritius": {"count": 3, "average_age": 25}
    },

    "shipyards": {
        "Hyundai Heavy Industries (HHI), Ulsan": {
            "is_busy": True,
            "current_project_start": date(2025, 5, 10),
            "current_project_end": date(2026, 1, 15),
            "project_category": "Commercial",
            "allowed_categories": ["Commercial", "Oil & Gas", "Offshore Energy", "LNG", "Bulk Carrier"]
        },
        "Daewoo Shipbuilding & Marine Engineering (DSME), Okpo": {
            "is_busy": True,
            "current_project_start": date(2025, 3, 15),
            "current_project_end": date(2025, 12, 30),
            "project_category": "Offshore Energy",
            "allowed_categories": ["Offshore Energy", "Naval", "Submarine", "Commercial", "LNG"]
        },
        "Samsung Heavy Industries, Geoje": {
            "is_busy": False,
            "current_project_start": None,
            "allowed_categories": ["Commercial", "Offshore Energy", "LNG", "Oil & Gas"]
        },
        "China State Shipbuilding Corporation (CSSC), Shanghai": {
            "is_busy": True,
            "current_project_start": date(2025, 6, 1),
            "current_project_end": date(2026, 3, 15),
            "project_category": "Naval",
            "allowed_categories": ["Naval", "Submarine", "Commercial", "Defense"]
        },
        "Dalian Shipbuilding Industry Company (DSIC), Dalian": {
            "is_busy": True,
            "current_project_start": date(2025, 4, 20),
            "current_project_end": date(2026, 2, 5),
            "project_category": "Commercial",
            "allowed_categories": ["Commercial", "Oil & Gas", "Container Ship", "LNG"]
        },
        "Jiangnan Shipyard, Shanghai": {
            "is_busy": False,
            "current_project_start": None,
            "allowed_categories": ["Commercial", "LNG", "Naval"]
        },
        "Guangzhou Shipyard International": {
            "is_busy": True,
            "current_project_start": date(2025, 7, 5),
            "current_project_end": date(2026, 6, 30),
            "project_category": "Defense",
            "allowed_categories": ["Defense", "Naval", "Commercial"]
        },
        "Mitsubishi Heavy Industries, Nagasaki & Kobe": {
            "is_busy": True,
            "current_project_start": date(2025, 2, 28),
            "current_project_end": date(2025, 12, 1),
            "project_category": "Cruise",
            "allowed_categories": ["Cruise", "Naval", "Submarine", "Commercial"]
        },
        "Imabari Shipbuilding, Ehime": {
            "is_busy": False,
            "current_project_start": None,
            "allowed_categories": ["Bulk Carrier", "Commercial", "Container Ship"]
        },
        "Oshima Shipbuilding, Saikai": {
            "is_busy": True,
            "current_project_start": date(2025, 5, 22),
            "current_project_end": date(2026, 2, 1),
            "project_category": "Commercial",
            "allowed_categories": ["Bulk Carrier", "Commercial"]
        },
        "Fincantieri, Italy": {
            "is_busy": True,
            "current_project_start": date(2025, 1, 12),
            "current_project_end": date(2026, 1, 12),
            "project_category": "Cruise",
            "allowed_categories": ["Cruise", "Naval", "Defense", "Submarine"]
        },
        "Meyer Werft, Germany": {
            "is_busy": False,
            "current_project_start": None,
            "allowed_categories": ["Cruise", "Ferry", "Luxury Yachts"]
        },
        "Navantia, Spain": {
            "is_busy": True,
            "current_project_start": date(2025, 8, 1),
            "current_project_end": date(2026, 5, 20),
            "project_category": "Naval",
            "allowed_categories": ["Naval", "Submarine", "Defense"]
        },
        "Huntington Ingalls Industries, Virginia & Mississippi": {
            "is_busy": True,
            "current_project_start": date(2025, 1, 3),
            "current_project_end": date(2026, 3, 31),
            "project_category": "Defense",
            "allowed_categories": ["Defense", "Naval", "Submarine"]
        },
        "General Dynamics NASSCO, San Diego": {
            "is_busy": True,
            "current_project_start": date(2025, 2, 17),
            "current_project_end": date(2025, 11, 17),
            "project_category": "Commercial",
            "allowed_categories": ["Commercial", "Fleet Replenishment", "Tanker"]
        },
        "Bath Iron Works, Maine": {
            "is_busy": False,
            "current_project_start": None,
            "allowed_categories": ["Naval", "Defense"]
        },
        "Sevmash, Severodvinsk": {
            "is_busy": True,
            "current_project_start": date(2025, 3, 1),
            "current_project_end": date(2026, 8, 1),
            "project_category": "Naval",
            "allowed_categories": ["Submarine", "Naval"]
        },
        "Admiralty Shipyards, St. Petersburg": {
            "is_busy": True,
            "current_project_start": date(2025, 6, 12),
            "current_project_end": date(2026, 4, 10),
            "project_category": "Submarine",
            "allowed_categories": ["Submarine", "Naval", "Research"]
        },
        "Cochin Shipyard, Kochi": {
            "is_busy": True,
            "current_project_start": date(2025, 7, 20),
            "current_project_end": date(2026, 5, 15),
            "project_category": "Defense",
            "allowed_categories": ["Defense", "Naval", "Commercial"]
        },
        "Garden Reach Shipbuilders & Engineers, Kolkata": {
            "is_busy": True,
            "current_project_start": date(2025, 8, 15),
            "current_project_end": date(2026, 6, 10),
            "project_category": "Naval",
            "allowed_categories": ["Naval", "Patrol", "Defense"]
        },
        "Estaleiro Atlântico Sul, Pernambuco": {
            "is_busy": True,
            "current_project_start": date(2025, 6, 5),
            "current_project_end": date(2026, 4, 30),
            "project_category": "Oil & Gas",
            "allowed_categories": ["Oil & Gas", "Commercial", "LNG"]
        },
        "RMK Marine, Istanbul": {
            "is_busy": True,
            "current_project_start": date(2025, 7, 1),
            "current_project_end": date(2026, 3, 1),
            "project_category": "Luxury Yachts",
            "allowed_categories": ["Luxury Yachts", "Ferries", "Small Naval", "Commercial"]
        },
        "Irving Shipbuilding, Canada": {
            "is_busy": True,
            "current_project_start": date(2025, 8, 10),
            "current_project_end": date(2026, 7, 10),
            "project_category": "Defense",
            "allowed_categories": ["Defense", "Naval", "Patrol"]
        },
        "DCD Marine, South Africa": {
            "is_busy": True,
            "current_project_start": date(2025, 4, 25),
            "current_project_end": date(2026, 1, 25),
            "project_category": "Commercial",
            "allowed_categories": ["Commercial", "Support Vessels", "Patrol"]
        }
    }

}


# Typical project durations (in days) for categories - you can tune this
PROJECT_DURATIONS = {
    "bulk_carrier": 365,
    "container_ship": 365,
    "general_cargo": 400,
    "oil_tanker": 365,
    "other_vessels": 300,
    "tugboats": 180,
    "fishing_vessels_large": 250,
    "cruise_ships": 450,
    "lng_carriers": 365,
    "lpg_carriers": 365,
    "offshore_support_vessels": 300,
    "research_vessels": 365,
    "ro_ro_ships": 365,
    "naval": 500,
    "defense": 500,
    "submarine": 600,
    "commercial": 365,
    "cruise": 450,
    "oil_and_gas": 400,
    "luxury_yachts": 200,
}

# Constants for replacement age window
MIN_REPLACE_AGE = 30
MAX_REPLACE_AGE = 35


# ----------------------------------------
# Data Classes
# ----------------------------------------

@dataclass
class ShipCategory:
    count: int
    average_age: float

@dataclass
class Shipyard:
    is_busy: bool
    current_project_start: Optional[date]
    current_project_end: Optional[date]
    project_category: Optional[str]
    project_category_key: Optional[str] = None
    lock: threading.Lock = field(default_factory=threading.Lock)
    allowed_categories: Optional[List[str]] = None

    def free_if_project_completed(self, current_date: date) -> bool:
        if self.is_busy and self.current_project_end and self.current_project_end <= current_date:
            self.is_busy = False
            return True
        return False

class FleetData:
    def __init__(self, merchant: Dict[str, ShipCategory], other: Dict[str, ShipCategory], naval: Dict[str, ShipCategory]):
        self.merchant = merchant
        self.other = other
        self.naval = naval

    def daily_age_increment(self):
        for cat_dict in [self.merchant, self.other]:
            for data in cat_dict.values():
                data.average_age += 1 / 365
        for data in self.naval.values():
            data.average_age += 1/365

    @staticmethod
    def calculate_due(count: int, avg_age: float) -> int:
        if avg_age < MIN_REPLACE_AGE:
            return 0
        if MIN_REPLACE_AGE <= avg_age <= MAX_REPLACE_AGE:
            factor = (avg_age - MIN_REPLACE_AGE) / (MAX_REPLACE_AGE - MIN_REPLACE_AGE)
            return int(count * factor)
        return count

    @staticmethod
    def estimate_due_for_replacement(categories: Dict[str, ShipCategory], prefix: str) -> Dict[str, int]:
        due = {}
        for category, data in categories.items():
            due_count = FleetData.calculate_due(data.count, data.average_age)
            if due_count > 0:
                key = f"{prefix}_{category.lower().replace(' ', '_')}"
                due[key] = due_count
        return due

    def estimate_naval_due(self) -> Dict[str, int]:
        total_due = sum(
            self.calculate_due(data.count, data.average_age)
            for data in self.naval.values()
        )
        return {"naval": total_due} if total_due > 0 else {}

    def ship_replaced(self, category_key: str):
        prefix_removed = category_key
        found = False
        if category_key.startswith("merchant_"):
            prefix_removed = category_key[len("merchant_"):]
            cat_dict = self.merchant
            found = True
        elif category_key.startswith("other_"):
            prefix_removed = category_key[len("other_"):]
            cat_dict = self.other
            found = True
        elif category_key == "naval":
            return
        
        if not found or prefix_removed not in cat_dict:
            return

        data = cat_dict[prefix_removed]
        if data.count == 0:
            return

        total_age_of_fleet = data.average_age * data.count
        data.count -= 1
        
        if data.count > 0:
            new_total_age = total_age_of_fleet - MAX_REPLACE_AGE 
            data.average_age = new_total_age / data.count
        else:
            data.average_age = 0
            
class Controller:
    def __init__(self, fleet_data: FleetData, shipyards: Dict[str, Shipyard]):
        self.fleet_data = fleet_data
        self.shipyards = shipyards
        self.backlog_queue: List[str] = []
        self.backlog_lock = threading.Lock()
        self.current_date: date = date(2025, 1, 1)
        self.day_advanced_event = threading.Event()
        self.shipyard_replacement_stats: Dict[str, Dict[str, int]] = {yard: defaultdict(int) for yard in shipyards}
        
        # New, high-performance aging model
        self.replacement_event_queue: Dict[date, List[str]] = defaultdict(list)
        self._init_replacement_events()

    def _init_replacement_events(self):
        # A simple model to get a better age distribution
        def get_age_distribution(count, avg_age):
            ages = []
            for _ in range(count):
                # Distribute ages with a wider range around the average
                age = random.uniform(max(0, avg_age - 15), avg_age + 15)
                ages.append(age)
            return ages
        
        # Calculate replacement dates for all initial ships
        for fleet_dict, prefix in [(self.fleet_data.merchant, "merchant"), (self.fleet_data.other, "other"), (self.fleet_data.naval, "naval")]:
            for cat, data in fleet_dict.items():
                if data.count > 0:
                    ages = get_age_distribution(data.count, data.average_age)
                    
                    for age in ages:
                        days_until_replacement = int((MAX_REPLACE_AGE - age) * 365)
                        if days_until_replacement > 0:
                            replacement_date = self.current_date + timedelta(days=days_until_replacement)
                            cat_key = f"{prefix}_{cat.lower().replace(' ', '_')}"
                            self.replacement_event_queue[replacement_date].append(cat_key)

    def _add_new_ship_to_queue(self, category_key: str):
        # When a new ship is completed, it's a new asset with age 0.
        # It will be due for replacement far in the future.
        replacement_date = self.current_date + timedelta(days=MAX_REPLACE_AGE * 365)
        self.replacement_event_queue[replacement_date].append(category_key)

    def advance_day(self):
        self.current_date += timedelta(days=1)
        
        with self.backlog_lock:
            # Check for any ships due for replacement today
            if self.current_date in self.replacement_event_queue:
                self.backlog_queue.extend(self.replacement_event_queue[self.current_date])
                # We can delete the key since we've processed it
                del self.replacement_event_queue[self.current_date]

        if self.current_date.day == 1:
            print(f"[{self.current_date}] 📦 Current backlog: {len(self.backlog_queue)}")
        
        self.day_advanced_event.set()

    def assign_project(self, shipyard_name: str) -> Optional[Tuple[str, str]]:
        yard = self.shipyards[shipyard_name]
        allowed_normalized = [
            c.lower().replace(' ', '_').replace('&', 'and') for c in yard.allowed_categories
        ] if yard.allowed_categories else []

        with self.backlog_lock:
            if not self.backlog_queue:
                return None

            available_projects = [
                item for item in self.backlog_queue if any(cat in item for cat in allowed_normalized)
            ]
            
            if not available_projects:
                return None

            project_key = available_projects[0]
            self.backlog_queue.remove(project_key)
                    
            if '_' in project_key:
                _, base_cat = project_key.split('_', 1)
            else:
                base_cat = project_key

            project_name = base_cat.replace('_', ' ').title().replace('And', '&')
            
            return project_name, project_key

    def complete_project(self, shipyard_name: str, category_name: str, category_key: str):
        self.shipyard_replacement_stats[shipyard_name][category_name] += 1
        with self.backlog_lock:
            self._add_new_ship_to_queue(category_key)
        print(f"[{self.current_date}] ✅ Shipyard '{shipyard_name}' completed '{category_name}'.")

    def print_shipyard_replacement_stats(self):
        print("\n=== Shipyard Replacement Statistics ===")
        for yard, stats in self.shipyard_replacement_stats.items():
            if stats:
                print(f"\n{yard}:")
                for category, count in stats.items():
                    print(f"  - {category}: {count} ships replaced")
            else:
                print(f"\n{yard}: No ships replaced yet")


class ShipyardThread(threading.Thread):
    def __init__(self, yard_name: str, controller: Controller):
        super().__init__(daemon=True)
        self.yard_name = yard_name
        self.controller = controller

    def run(self):
        while True:
            self.controller.day_advanced_event.wait()
            
            yard = self.controller.shipyards[self.yard_name]
            
            with yard.lock:
                if yard.is_busy and yard.free_if_project_completed(self.controller.current_date):
                    self.controller.complete_project(self.yard_name, yard.project_category, yard.project_category_key)
                    yard.current_project_start = None
                    yard.current_project_end = None
                    yard.project_category = None
                    yard.project_category_key = None

                if not yard.is_busy:
                    project_data = self.controller.assign_project(self.yard_name)
                    if project_data:
                        project_name, project_key = project_data
                        category_name_for_duration = project_name.lower().replace(" ", "_").replace("&", "and")
                        duration = PROJECT_DURATIONS.get(category_name_for_duration, 365)
                        start = self.controller.current_date
                        end = start + timedelta(days=duration)
                        
                        yard.is_busy = True
                        yard.current_project_start = start
                        yard.current_project_end = end
                        yard.project_category = project_name
                        yard.project_category_key = project_key

                        print(f"[{start}] 🏗️ Shipyard '{self.yard_name}' started '{project_name}' (ends {end})")
            
            self.controller.day_advanced_event.clear()

# ----------------------------------------
# Initialization
# ----------------------------------------

def main():
    merchant = {k: ShipCategory(**v) for k, v in World_fleet["merchant_fleet_breakdown"].items()}
    other = {k: ShipCategory(**v) for k, v in World_fleet["other_vessel_types"].items()}
    naval = {k: ShipCategory(**v) for k, v in World_fleet["naval_forces_by_country"].items()}

    fleet_data = FleetData(merchant, other, naval)

    shipyards = {
        name: Shipyard(
            is_busy=info["is_busy"],
            current_project_start=info.get("current_project_start"),
            current_project_end=info.get("current_project_end"),
            project_category=info.get("project_category"),
            allowed_categories=info.get("allowed_categories")
        )
        for name, info in World_fleet["shipyards"].items()
    }

    # FIX: Correctly initialize project_category_key for initially busy shipyards
    for name, info in World_fleet["shipyards"].items():
        if info["is_busy"]:
            yard = shipyards[name]
            project_key = info["project_category"].lower().replace(" ", "_").replace("&", "and")
            if project_key == "offshore_energy":
                project_key = "offshore_support_vessels"
            if project_key == "cruise":
                project_key = "cruise_ships"
            if project_key == "tanker":
                project_key = "oil_tanker"
            if project_key == "bulk_carrier":
                project_key = "bulk_carrier"
            if project_key == "container_ship":
                project_key = "container_ship"
            if project_key == "oil_&_gas":
                project_key = "oil_and_gas"
            
            yard.project_category_key = project_key

    controller = Controller(fleet_data, shipyards)

    for name in shipyards:
        thread = ShipyardThread(name, controller)
        thread.start()

    # Simulate 25 years
    for _ in range(25 * 365):
        controller.advance_day()

    print("\n📦 Final backlog:")
    with controller.backlog_lock:
        backlog_counts = defaultdict(int)
        for item in controller.backlog_queue:
            backlog_counts[item] += 1
        
        for cat, count in backlog_counts.items():
            print(f" - {cat}: {count}")
        print(f"Total backlog: {len(controller.backlog_queue)}")

    controller.print_shipyard_replacement_stats()

if __name__ == "__main__":
    main()