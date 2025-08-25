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
    "China Shipbuilding Group (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Offshore",
        "Subsea"
      ]
    },
    "Hyundai Heavy Industries (HHI), South Korea": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "LNG",
        "Naval",
        "Bulk Carrier"
      ]
    },
    "Daewoo Shipbuilding & Marine Engineering (DSME), South Korea": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore Energy",
        "Submarine",
        "LNG"
      ]
    },
    "Samsung Heavy Industries (SHI), South Korea": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "LNG",
        "FPSO",
        "Container Ship",
        "Offshore"
      ]
    },
    "Japan Marine United (JMU), Japan": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Offshore",
        "LNG",
        "Submarine"
      ]
    },
    "Imabari Shipbuilding, Japan": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier",
        "Container Ship",
        "Tanker"
      ]
    },
    "Fincantieri, Italy": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise",
        "Naval",
        "Submarine"
      ]
    },
    "Sumitomo Heavy Industries, Japan": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier",
        "Special Vessels"
      ]
    },
    "Damen Shipyards Group, Netherlands": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol",
        "Ferries",
        "Offshore Support",
        "Tug"
      ]
    },
    "Sembcorp Marine, Singapore": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Green Shipping"
      ]
    },
    "Kawasaki Shipbuilding (Kobe, Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Tankers",
        "Ro-Ro",
        "Patrol"
      ]
    },
    "Mitsui E&S Shipbuilding (Tamano, Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier",
        "LNG",
        "Patrol",
        "Fishing"
      ]
    },
    "Mitsubishi Heavy Industries (Nagasaki & Kobe, Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "LNG",
        "Oil Tankers",
        "Cruise",
        "Naval"
      ]
    },
    "Yantai Raffles Shipyard (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Platform",
        "Commercial"
      ]
    },
    "Jiangnan Shipyard (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Submarine"
      ]
    },
    "Damen Galați (Romania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Offshore",
        "Tug",
        "Research"
      ]
    },
    "BLRT Grupp (Estonia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair",
        "Offshore"
      ]
    },
    "Westcon Yards AS (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Repair"
      ]
    },
    "Palumbo Group (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial",
        "Superyachts"
      ]
    },
    "Ingalls Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial",
        "Rigs",
        "Cruise"
      ]
    },
    "BAE Systems Maritime (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Harland & Wolff (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Defense"
      ]
    },
    "Karachi Shipyard (Pakistan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Mazagaon Dock (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial",
        "Submarine"
      ]
    },
    "Aker Solutions (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Odense Maritime Technology (Denmark)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Submarine"
      ]
    },
    "Remontowa Shipbuilding (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "CSBC Corporation (Taiwan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Malaysia Marine & Heavy Engineering (Malaysia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial"
      ]
    },
    "PT PAL Indonesia (Indonesia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Austal (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Ferries"
      ]
    },
    "ASTIMAR Tampico (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "ASMAR (Chile)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASENAV (Chile)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Atlântico Sul Shipyard (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Astillero Rio Santiago (Argentina)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "SPI Astilleros (Argentina)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "SIMA Callao (Peru)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASTINAVE (Ecuador)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Ba Son Shipyard (Vietnam)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Cochin Shipyard (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Garden Reach (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Estaleiro Atlântico Sul (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "RMK Marine (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Irving Shipbuilding (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "DCD Marine (South Africa)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "CSSC Jiangnan Shipyard (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "LNG"
      ]
    },
    "Hudong–Zhonghua Shipbuilding (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "LNG",
        "Submarine"
      ]
    },
    "Shanghai Waigaoqiao Shipbuilding (SWS) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship",
        "Bulk Carrier"
      ]
    },
    "Dalian Shipbuilding Industry (DSIC) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "Tanker"
      ]
    },
    "Guangzhou Shipyard International (GSI) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ro-Pax",
        "Tanker"
      ]
    },
    "Qingdao Beihai Shipbuilding (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "China Merchants Heavy Industry (Shenzhen) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Repair"
      ]
    },
    "China Merchants Heavy Industry (Jiangsu) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Yangzijiang Shipbuilding (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship",
        "Bulk Carrier"
      ]
    },
    "New Times Shipbuilding (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tanker",
        "Bulk Carrier"
      ]
    },
    "COSCO Shipping Heavy Industry (Zhoushan) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial",
        "Offshore"
      ]
    },
    "COSCO Shipping Heavy Industry (Nantong) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Wuchang Shipbuilding Industry Group (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Bohai Shipbuilding Heavy Industry (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial",
        "Submarine"
      ]
    },
    "Zhejiang Shipping Group Yard (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Mawei Shipyard (Fuzhou) (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Huangpu Wenchong Shipyard (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "CIMC Raffles Yantai (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial",
        "FPSO"
      ]
    },
    "Jiangsu New Yangzi Shipbuilding (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship"
      ]
    },
    "NACKS – Nantong COSCO KHI Ship Engineering (China)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship",
        "Bulk Carrier"
      ]
    },
    "HD Hyundai Mipo Dockyard (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tanker",
        "Container Ship"
      ]
    },
    "Hyundai Samho Heavy Industries (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship",
        "LNG"
      ]
    },
    "Hanwha Ocean (ex-DSME) (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval",
        "LNG"
      ]
    },
    "STX Offshore & Shipbuilding (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "Daehan Shipbuilding (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tanker",
        "Bulk Carrier"
      ]
    },
    "Sungdong Shipbuilding (South Korea)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "Oshima Shipbuilding (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "Tsuneishi Shipbuilding (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "Namura Shipbuilding (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier",
        "Tanker"
      ]
    },
    "Shin Kurushima Dockyard (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Container Ship"
      ]
    },
    "Onomichi Dockyard (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulker",
        "Tanker"
      ]
    },
    "Kure Shipyard (JMU) (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Mitsubishi Heavy Industries – Nagasaki Shipyard (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise",
        "LNG"
      ]
    },
    "Kawasaki Heavy Industries – Sakaide (Japan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "LNG",
        "Tanker"
      ]
    },
    "CSBC Kaohsiung Shipyard (Taiwan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "CSBC Keelung Shipyard (Taiwan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Seatrium Tuas Yard (Singapore)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial",
        "Repair"
      ]
    },
    "Seatrium Benoi Yard (Singapore)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial",
        "Repair"
      ]
    },
    "PaxOcean Tuas (Singapore)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Offshore",
        "Commercial"
      ]
    },
    "Damen Shiprepair Singapore (Singapore)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "PT PAL Surabaya (Indonesia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASL Shipyard Batam (Indonesia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Repair"
      ]
    },
    "PaxOcean Graha (Indonesia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial",
        "Repair"
      ]
    },
    "Batamec Shipyard (Indonesia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "MMHE – Malaysia Marine & Heavy Engineering (Malaysia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial"
      ]
    },
    "Boustead Naval Shipyard Lumut (Malaysia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Nam Cheong Dockyard (Malaysia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Shin Yang Shipyard (Malaysia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Damen Song Cam (Vietnam)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tug",
        "Patrol"
      ]
    },
    "VARD Vung Tau (Vietnam)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Cruise"
      ]
    },
    "Ha Long Shipyard (Vietnam)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Z189 – Song Thu Corporation (Vietnam)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Austal Philippines (Balamban) (Philippines)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Tsuneishi Heavy Industries (Cebu) (Philippines)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Bulk Carrier"
      ]
    },
    "Subic Shipyard (ex-Hanjin) (Philippines)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Bangkok Dock (Thailand)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Marsun Shipyard (Thailand)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "Colombo Dockyard (Sri Lanka)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair",
        "Offshore"
      ]
    },
    "Western Marine Shipyard (Bangladesh)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Ananda Shipyard & Slipways (Bangladesh)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Mazagon Dock Shipbuilders (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine",
        "Commercial"
      ]
    },
    "Garden Reach Shipbuilders & Engineers (GRSE) (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Cochin Shipyard Limited (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Goa Shipyard Limited (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Hindustan Shipyard Ltd (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "L&T Shipbuilding Kattupalli (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "ABG Shipyard (India)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Karachi Shipyard & Engineering Works (Pakistan)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Drydocks World Dubai (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Offshore",
        "Commercial"
      ]
    },
    "Abu Dhabi Ship Building (ADSB) (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Albwardy Damen (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Grandweld Shipyards (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "ASRY – Arab Shipbuilding & Repair Yard (Bahrain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "International Maritime Industries (Saudi Arabia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Zamil Offshore (Saudi Arabia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Nakilat Damen Shipyards Qatar (Qatar)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Asyad Drydock (Duqm) (Oman)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial",
        "Offshore"
      ]
    },
    "ISOICO – Iran Shipbuilding & Offshore Industries (Iran)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "SADRA Shipbuilding (Iran)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial"
      ]
    },
    "Israel Shipyards (Israel)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Alexandria Shipyard (Egypt)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Port Said Shipyard (Egypt)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Suez Shipyard (Egypt)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Damen Shipyards Cape Town (South Africa)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Southern African Shipyards (South Africa)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Sandock Austral Shipyards (South Africa)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Namdock – Elgin Brown & Hamer (Namibia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Nigerdock (Nigeria)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore",
        "Repair"
      ]
    },
    "Naval Dockyard Limited Lagos (Nigeria)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Tema Shipyard (Ghana)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Dakar Shipyard (Senegal)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Paenal Yard (Angola)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Commercial"
      ]
    },
    "Meyer Turku (Finland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Rauma Marine Constructions (RMC) (Finland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Helsinki Shipyard (Finland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Arctic"
      ]
    },
    "Uudenkaupungin Työvene (Finland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "Saab Kockums Karlskrona (Sweden)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Oskarshamn Shipyard (Sweden)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Fayard Odense (Denmark)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Karstensens Skibsværft (Denmark)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Fishing"
      ]
    },
    "Orskov Yard (Denmark)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Meyer Werft Papenburg (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "ThyssenKrupp Marine Systems Kiel (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Lürssen Werft (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Yacht"
      ]
    },
    "Blohm+Voss (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Yacht",
        "Naval"
      ]
    },
    "German Naval Yards Kiel (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Flensburger Schiffbau-Gesellschaft (FSG) (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ro-Ro"
      ]
    },
    "Abeking & Rasmussen (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht",
        "Naval"
      ]
    },
    "Fassmer (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "Damen Shipyards Vlissingen (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Damen Shipyards Gorinchem (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tug"
      ]
    },
    "Royal IHC (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Dredgers"
      ]
    },
    "Heesen Yachts (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Oceanco (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Feadship – Royal De Vries (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Feadship – Royal Van Lent (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Damen Yachting – Amels (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Ferus Smit (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Royal Niestern Sander (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Chantiers de l'Atlantique (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise",
        "Naval"
      ]
    },
    "Naval Group Brest (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Naval Group Lorient (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Naval Group Cherbourg (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Naval Group Toulon (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "CMN – Constructions Mécaniques de Normandie (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Patrol"
      ]
    },
    "Piriou Shipyard (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "OCEA Les Sables-d’Olonne (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Patrol",
        "Commercial"
      ]
    },
    "Socarenam (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Patrol",
        "Commercial"
      ]
    },
    "BAE Systems – Barrow-in-Furness (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "BAE Systems – Govan (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "BAE Systems – Scotstoun (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Babcock Rosyth (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Cammell Laird (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Harland & Wolff Belfast (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Harland & Wolff Appledore (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Ferguson Marine (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "A&P Falmouth (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "A&P Tyne (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "A&P Tees (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Damen Shiprepair Harlingen (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Navantia Ferrol (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Navantia Cartagena (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Navantia Cadiz / Puerto Real (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Navantia San Fernando (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Zamakona Yards Bilbao (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Zamakona Yards Las Palmas (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Offshore"
      ]
    },
    "Astilleros Gondán (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Astilleros Armon (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tug",
        "Offshore"
      ]
    },
    "Astican – Astilleros de Canarias (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Offshore"
      ]
    },
    "Metalships & Docks (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "WestSea Viana do Castelo (Portugal)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Lisnave – Mitrena (Portugal)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Navalrocha (Portugal)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Fincantieri Monfalcone (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Fincantieri Marghera (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Fincantieri Sestri Ponente (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Fincantieri Ancona (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Cruise"
      ]
    },
    "Fincantieri Palermo (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Fincantieri Castellammare di Stabia (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Fincantieri Riva Trigoso (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Fincantieri Muggiano (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Cantiere Navale Vittoria (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Patrol",
        "Commercial"
      ]
    },
    "Cantiere Navale Palumbo (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Superyachts"
      ]
    },
    "Remontowa Gdańsk (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "CRIST Shipyard (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Gdańsk Shipyard (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Stocznia Szczecińska (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Damen Shipyards Mangalia (Romania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Damen Shipyards Galați (Romania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "VARD Tulcea (Romania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Uljanik Shipyard (Croatia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "3. Maj Shipyard (Croatia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Brodosplit (Croatia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Western Shipyard – BLRT (Lithuania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Riga Shipyard (Latvia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Tallinn Shipyard – BLRT (Estonia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Sevmash (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Admiralty Shipyards (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Baltiysky Zavod (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Icebreaker"
      ]
    },
    "Yantar Shipyard (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Zvezda Shipbuilding Complex (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Vyborg Shipyard (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ice-class"
      ]
    },
    "Black Sea Shipyard (Ukraine)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Ocean Shipyard Mykolaiv (Ukraine)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Kuznya na Rybalskomu (Ukraine)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Newport News Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "General Dynamics Electric Boat – Groton (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "General Dynamics Electric Boat – Quonset Point (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "General Dynamics NASSCO San Diego (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Philly Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Fincantieri Marinette Marine (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Fincantieri Bay Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Ingalls Shipbuilding Pascagoula (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval"
      ]
    },
    "Austal USA (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "BAE Systems Jacksonville Ship Repair (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "BAE Systems San Diego Ship Repair (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Vigor Shipyards Portland (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Vigor Shipyards Seattle (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Vigor Ketchikan (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Bollinger Shipyards (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Bollinger Mississippi Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Eastern Shipbuilding Group (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Conrad Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Thoma-Sea Marine Constructors (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Master Boat Builders (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Metal Shark (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "Dakota Creek Industries (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Nichols Brothers Boat Builders (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Gladding-Hearn Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Patrol"
      ]
    },
    "All American Marine (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Colonna's Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Norfolk Naval Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Puget Sound Naval Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Portsmouth Naval Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Pearl Harbor Naval Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "Bay Ship & Yacht (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "VT Halter / Bollinger Pascagoula (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Keppel AmFELS (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Great Lakes Shipyard (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Detyens Shipyards (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Irving Halifax Shipyard (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Seaspan Vancouver Shipyards (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Seaspan Victoria Shipyards (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Davie Shipbuilding (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Heddle Shipyards (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Chantier Naval Forillon (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Ocean Group Shipyard Quebec (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "ASTIMAR 1 Tampico (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASTIMAR 3 Coatzacoalcos (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASTIMAR 6 Guaymas (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASTIMAR 20 Salina Cruz (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Talleres Navales del Golfo (TNG) Veracruz (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "SIMSA Shipyard (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Damen Shiprepair Curaçao (Curaçao)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Grand Bahama Shipyard (Bahamas)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Caribbean Dockyard & Engineering (Trinidad & Tobago)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Estaleiro Rio Grande (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Estaleiro Mauá (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Wilson Sons Shipyard Guarujá (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tug"
      ]
    },
    "Ecovix (Brazil)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "ASENAV Valdivia (Chile)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "ASMAR Talcahuano (Chile)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "COTECMAR Cartagena (Colombia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "ASTINAVE EP (Ecuador)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "SIMA Chimbote (Peru)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "SIMA Iquitos (Peru)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "TANDANOR (Argentina)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Contessi Shipyard (Argentina)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Fishing"
      ]
    },
    "Tsakos Industrias Navales (Uruguay)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "DIANCA – Diques y Astilleros Nacionales (Venezuela)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Austal Henderson (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "BAE Systems Henderson (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Repair"
      ]
    },
    "ASC Osborne (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Submarine"
      ]
    },
    "Incat Tasmania (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Ferries"
      ]
    },
    "Civmec Henderson (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Forgacs – Newcastle (Australia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "NZ Ship Repair – Devonport (New Zealand)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Stabicraft / Marine Industrial Park (New Zealand)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial"
      ]
    },
    "Sedef Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Naval"
      ]
    },
    "Sefine Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Cemre Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Tersan Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Anadolu Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Istanbul Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Dearsan Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Yonca-Onuk Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Patrol",
        "Naval"
      ]
    },
    "Desan Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Sanmar Shipyards (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Tug"
      ]
    },
    "Benetti Livorno (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "CRN Ancona (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Sanlorenzo La Spezia (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Baglietto La Spezia (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Ferretti Ancona (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "Damen Shiprepair Amsterdam (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Damen Shiprepair Rotterdam (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Icon Yachts Harlingen (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Yacht"
      ]
    },
    "VARD Brattvaag (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "VARD Søviknes (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "VARD Aukra (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Ulstein Verft (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Kleven Yard (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Havyard Leirvik (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Fitjar Mekaniske Verksted (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Aibel Haugesund Yard (Norway)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Offshore",
        "Repair"
      ]
    },
    "Hellenic Shipyards Skaramangas (Greece)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Elefsis Shipyards (Greece)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Naval",
        "Commercial"
      ]
    },
    "Neorion Syros Shipyards (Greece)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Piraeus Ship Repair Zone (Greece)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Kiziltoprak Shipyard (Cyprus)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Damen Shiprepair Brest (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Harland & Wolff Belfast Yard (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Offshore"
      ]
    },
    "Damen Shiprepair Vlissingen (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Damen Shiprepair Den Helder (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "BMA Shipyard Antwerp (Belgium)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Verolme Cork Dockyard (Ireland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Repair",
        "Commercial"
      ]
    },
    "Harland & Wolff Methil (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Harland & Wolff Arnish (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Damen Shiprepair Dunkerque (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "SMS Group Lowestoft (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Blyth Tall Ship Yard (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Harwich Navyard (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Plymouth Appledore Facility (UK)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros Balenciaga (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Armon Gijón (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Armon Vigo (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros Murueta (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Armon Navia (Spain)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Lindenau Werft (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Peters Werft (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Norderwerft (Germany)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Chantiers Piriou Concarneau (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "CMI La Rochelle (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "La Ciotat Shipyards (France)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Royal Huisman (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Damen Hardinxveld (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Koninklijke De Vries Scheepsbouw (Netherlands)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Rosetti Marino (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Codecasa Viareggio (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Cantieri Navali Vittoria (Italy)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Karstensen Skagen (Denmark)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Ornskoldsvik Shipyard (Sweden)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Gryfia Shiprepair Yard (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Nauta Shiprepair Yard (Poland)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Baltija Shipyard (Lithuania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "BLRT Western Baltija (Lithuania)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Kotor Shipyard (Montenegro)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "NCP Repair Šibenik (Croatia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Severnaya Verf (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Amur Shipbuilding Plant (Russia)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Nibulon Shipbuilding (Ukraine)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "ART Shipyard Tuzla (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Basaran Shipyard (Turkey)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Drydocks World Graha (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Fujairah Marine Services (UAE)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Alexandria Shipyard Ezz El Arab (Egypt)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Lagos Deep Offshore Logistics (LADOL) (Nigeria)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "VT Halter Pascagoula (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Senesco Marine (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Washburn & Doughty (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Blount Boats (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Silver Ships (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "SAFE Boats International (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Marinette Small Boat Works (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Halter Marine Repair (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Metal Trades Inc (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Port City Shipbuilding (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "JAG Alaska – Seward (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Portland Yacht Services (USA)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Ocean Industries – Isle-aux-Coudres (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Seaway Marine & Industrial (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Nanaimo Shipyard (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Shelburne Ship Repair (Canada)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros de Veracruz (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros Unidos de Veracruz (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros de Marina Cancun (Mexico)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros Ultrapetrol (Uruguay)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astillero SPI Mar del Plata (Argentina)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Arsenal de Marina de Guerra del Perú (Peru)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
    },
    "Astilleros y Maestranzas de la Armada Punta Arenas (Chile)": {
      "is_busy": False,
      "current_project_start": None,
      "current_project_end": None,
      "allowed_categories": [
        "Commercial",
        "Repair"
      ]
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