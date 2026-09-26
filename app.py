import uuid
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

destinations_by_id = {}
destinations_list = []

trips_by_id = {}
trips_list = []

activities_by_id = {}
activities_list = []

places_by_id = {}
places_list = []

packing_items_by_id = {}
packing_items_list = []

journal_entries_by_id = {}
journal_entries_list = []

def seed_data():
    destinations_by_id.clear()
    destinations_list.clear()
    trips_by_id.clear()
    trips_list.clear()
    activities_by_id.clear()
    activities_list.clear()
    places_by_id.clear()
    places_list.clear()
    packing_items_by_id.clear()
    packing_items_list.clear()
    journal_entries_by_id.clear()
    journal_entries_list.clear()

    seed_destinations = [
        ("dest_kyoto", "Kyoto", "Japan", "East Asia", "Ancient temples, traditional tea houses, bamboo groves, and vibrant autumn foliage.", "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80", ["Culture", "Food", "History"], 8500.0, 5),
        ("dest_paris", "Paris", "France", "Europe", "Iconic landmarks, world-class museums, romantic avenues, and culinary excellence.", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80", ["Culture", "Luxury", "Food"], 12000.0, 6),
        ("dest_bali", "Bali", "Indonesia", "Southeast Asia", "Tropical beaches, lush rice terraces, sacred temples, and serene wellness retreats.", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80", ["Beach", "Relaxation", "Nature"], 6000.0, 7),
        ("dest_kerala", "Kerala", "India", "South Asia", "Tranquil backwaters, palm-fringed beaches, tea plantations, and Ayurvedic heritage.", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80", ["Nature", "Relaxation", "Culture"], 4500.0, 5),
        ("dest_goa", "Goa", "India", "South Asia", "Golden sand beaches, Portuguese architecture, vibrant night markets, and seafood delicacies.", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80", ["Beach", "Relaxation", "Food"], 3500.0, 4),
        ("dest_manali", "Manali", "India", "South Asia", "Majestic Himalayan peaks, alpine forests, adventure sports, and scenic valleys.", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80", ["Adventure", "Nature"], 3800.0, 5),
        ("dest_dubai", "Dubai", "UAE", "Middle East", "Futuristic skyscrapers, desert safaris, luxury shopping malls, and artificial archipelagos.", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80", ["Luxury", "City", "Shopping"], 14000.0, 4),
        ("dest_singapore", "Singapore", "Singapore", "Southeast Asia", "Futuristic gardens, multicultural neighborhood dining, clean urban architecture, and wildlife reserves.", "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=800&q=80", ["City", "Food", "Culture"], 11000.0, 4),
        ("dest_ny", "New York", "USA", "North America", "Bustling metropolis, Broadway theater district, Central Park green space, and world-famous museums.", "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800&q=80", ["City", "Culture", "Food"], 16000.0, 5),
        ("dest_istanbul", "Istanbul", "Turkey", "Eurasia", "Where East meets West: grand mosques, historic bazaars, and Bosphorus strait cruises.", "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=800&q=80", ["Culture", "History", "Food"], 7000.0, 6)
    ]

    for d_id, name, country, region, desc, img, styles, daily_b, rec_days in seed_destinations:
        dest_item = {
            "id": d_id,
            "name": name,
            "country": country,
            "region": region,
            "description": desc,
            "image": img,
            "travel_styles": styles,
            "estimated_daily_budget": daily_b,
            "recommended_days": rec_days
        }
        destinations_by_id[d_id] = dest_item
        destinations_list.append(dest_item)

    # Seed 5 Initial Journeys across different destinations and statuses
    seed_trips = [
        ("TRIP-101", "Monsoon Kerala Escape", "dest_kerala", "Kerala", "India", "2026-10-10", "2026-10-14", 3, "Nature", "Upcoming"),
        ("TRIP-102", "Kyoto Autumn Temple Walk", "dest_kyoto", "Kyoto", "Japan", "2026-09-24", "2026-09-29", 2, "Culture", "In Progress"),
        ("TRIP-103", "Paris Art & Gourmet Odyssey", "dest_paris", "Paris", "France", "2026-11-05", "2026-11-11", 2, "Luxury", "Upcoming"),
        ("TRIP-104", "Bali Wellness & Beach Retreat", "dest_bali", "Bali", "Indonesia", "2026-08-01", "2026-08-07", 1, "Relaxation", "Completed"),
        ("TRIP-105", "Himalayan Manali Trek", "dest_manali", "Manali", "India", "2026-12-15", "2026-12-20", 4, "Adventure", "Upcoming")
    ]

    for t_id, t_name, d_id, d_name, country, s_date, e_date, travelers, style, status in seed_trips:
        trip_item = {
            "id": t_id,
            "name": t_name,
            "destination_id": d_id,
            "destination_name": d_name,
            "country": country,
            "start_date": s_date,
            "end_date": e_date,
            "travelers": travelers,
            "travel_style": style,
            "status": status,
            "created_at": datetime.now().isoformat()
        }
        trips_by_id[t_id] = trip_item
        trips_list.append(trip_item)

    # Seed activities for multiple journeys
    seed_acts = [
        ("TRIP-101", 1, "Airport Transfer & Fort Kochi Walk", "09:00", "Fort Kochi", "Transport", "2 hours", 1200.0, "Meet driver at arrival gate"),
        ("TRIP-101", 1, "Traditional Seafood Lunch at Waterfront", "13:00", "Kochi Harbor", "Food", "1.5 hours", 1800.0, "Try local fish curry meals"),
        ("TRIP-101", 1, "Sunset Chinese Fishing Nets Visit", "17:30", "Fort Kochi Beach", "Sightseeing", "1 hour", 300.0, "Great photography spot"),
        ("TRIP-101", 2, "Drive to Alleppey Houseboat Pier", "08:30", "Kochi to Alleppey", "Transport", "2 hours", 2500.0, "Private AC cab ride"),
        ("TRIP-101", 2, "Houseboat Check-in & Backwater Cruise", "11:30", "Vembanad Lake", "Leisure", "6 hours", 12000.0, "Includes onboard chef lunch & tea"),
        ("TRIP-101", 3, "Drive to Munnar Tea Gardens", "09:00", "Alleppey to Munnar", "Transport", "3.5 hours", 3200.0, "Scenic mountain route"),
        ("TRIP-101", 3, "Munnar Tea Museum & Plantation Tour", "15:00", "Tea Estate", "Culture", "2 hours", 600.0, "Tea tasting experience"),
        ("TRIP-102", 1, "Morning Walk through Fushimi Inari Torii", "08:00", "Fushimi Inari", "Sightseeing", "2.5 hours", 0.0, "Beat the crowds"),
        ("TRIP-102", 1, "Traditional Matcha & Sweet Workshop", "14:00", "Gion Teahouse", "Culture", "1.5 hours", 3500.0, "Kimono experience optional"),
        ("TRIP-102", 2, "Kinkaku-ji Golden Pavilion Tour", "10:00", "Kinkaku-ji", "Culture", "2 hours", 800.0, "Golden leaf reflections"),
        ("TRIP-103", 1, "Private Guided Tour of Louvre Masterpieces", "09:30", "Louvre Museum", "Culture", "3 hours", 4500.0, "Skip line tickets"),
        ("TRIP-103", 1, "Seine River Dinner Cruise", "20:00", "Pont Neuf", "Food", "2.5 hours", 9000.0, "3-course gourmet dining")
    ]

    for t_id, day, title, time_str, loc, cat, dur, cost, notes in seed_acts:
        a_id = f"ACT-{uuid.uuid4().hex[:6].upper()}"
        act_item = {
            "id": a_id,
            "trip_id": t_id,
            "day": day,
            "title": title,
            "time": time_str,
            "location": loc,
            "category": cat,
            "duration": dur,
            "estimated_cost": cost,
            "notes": notes
        }
        activities_by_id[a_id] = act_item
        activities_list.append(act_item)

    # Seed 35 Places with rich metadata and images
    seed_places = [
        ("dest_kerala", "Munnar Tea Gardens", "Nature", "Lush rolling green hills of tea plantations.", 200.0, "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=600&q=80"),
        ("dest_kerala", "Alleppey Backwaters Pier", "Attraction", "Scenic houseboat cruise launch point.", 500.0, "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=600&q=80"),
        ("dest_kerala", "Fort Kochi Chinese Fishing Nets", "Heritage", "Historic fishing structures along the Arabian sea shore.", 100.0, "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=600&q=80"),
        ("dest_kerala", "Periyar National Park", "Nature", "Wildlife sanctuary famous for elephants and lake cruises.", 650.0, "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=600&q=80"),
        ("dest_kyoto", "Fushimi Inari Shrine", "Culture", "Iconic path of thousands of vermilion torii gates.", 0.0, "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=600&q=80"),
        ("dest_kyoto", "Arashiyama Bamboo Grove", "Nature", "Towering green bamboo stalks creating a serene path.", 0.0, "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=600&q=80"),
        ("dest_kyoto", "Kinkaku-ji Golden Pavilion", "Culture", "Zen Buddhist temple covered in gold leaf over a pond.", 400.0, "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=600&q=80"),
        ("dest_kyoto", "Gion Geisha District", "Heritage", "Historic neighborhood with traditional wooden machiya townhouses.", 0.0, "https://images.unsplash.com/photo-1528164344705-47542687990d?auto=format&fit=crop&w=600&q=80"),
        ("dest_paris", "Louvre Museum", "Museum", "World famous art gallery featuring the Mona Lisa.", 1800.0, "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=600&q=80"),
        ("dest_paris", "Eiffel Tower Observatory", "Landmark", "Iconic iron tower offering panoramic views of Paris.", 2400.0, "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=600&q=80"),
        ("dest_paris", "Sainte-Chapelle", "Culture", "13th-century Gothic chapel with magnificent stained glass.", 1200.0, "https://images.unsplash.com/photo-1549144511-f099e773c147?auto=format&fit=crop&w=600&q=80"),
        ("dest_paris", "Montmartre & Sacré-Cœur", "Heritage", "Bohemian hilltop district overlooking the city skyline.", 0.0, "https://images.unsplash.com/photo-1509299349698-dd22323b5963?auto=format&fit=crop&w=600&q=80"),
        ("dest_bali", "Ubud Rice Terraces", "Nature", "Lush emerald green terraced rice fields of Tegallalang.", 150.0, "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=600&q=80"),
        ("dest_bali", "Tanah Lot Temple", "Culture", "Ancient Hindu shrine perched on an offshore rock formation.", 300.0, "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=600&q=80"),
        ("dest_bali", "Uluwatu Cliff Sunset", "Landmark", "Dramatic sea cliff views with traditional Kecak dance performances.", 500.0, "https://images.unsplash.com/photo-1552733407-2d2d4742f58e?auto=format&fit=crop&w=600&q=80"),
        ("dest_bali", "Sacred Monkey Forest Sanctuary", "Nature", "Sanctuary housing hundreds of long-tailed macaques.", 400.0, "https://images.unsplash.com/photo-1570789210967-2cac24afeb00?auto=format&fit=crop&w=600&q=80"),
        ("dest_goa", "Calangute & Baga Beach", "Beach", "Vibrant sandy coastline with water sports and beach shacks.", 0.0, "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600&q=80"),
        ("dest_goa", "Basilica of Bom Jesus", "Heritage", "UNESCO World Heritage site containing relics of St. Francis Xavier.", 0.0, "https://images.unsplash.com/photo-1587922546307-776227941871?auto=format&fit=crop&w=600&q=80"),
        ("dest_goa", "Dudhsagar Waterfalls", "Nature", "Four-tiered majestic waterfall cascading down western ghats.", 800.0, "https://images.unsplash.com/photo-1627894006596-9b986878b4b3?auto=format&fit=crop&w=600&q=80"),
        ("dest_goa", "Fontainhas Latin Quarter", "Culture", "Quaint Portuguese neighborhood with colorful heritage villas.", 0.0, "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=600&q=80"),
        ("dest_manali", "Solang Valley Adventure Hub", "Adventure", "Famous valley for paragliding, zorbing, and winter skiing.", 1500.0, "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=600&q=80"),
        ("dest_manali", "Hadimba Devi Temple", "Culture", "Historic wooden pagoda temple surrounded by cedar forest.", 50.0, "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=600&q=80"),
        ("dest_manali", "Rohtang Pass Viewpoint", "Nature", "High mountain pass offering breathtaking Himalayan snow vistas.", 1200.0, "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?auto=format&fit=crop&w=600&q=80"),
        ("dest_dubai", "Burj Khalifa Observation Deck", "Landmark", "World's tallest building with observation deck on 124th floor.", 4500.0, "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80"),
        ("dest_dubai", "Dubai Desert Conservation Reserve", "Adventure", "Dune bashing, camel riding, and traditional Bedouin dinner.", 3500.0, "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80"),
        ("dest_dubai", "Museum of the Future", "Museum", "Innovative architectural landmark celebrating futuristic tech.", 3200.0, "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?auto=format&fit=crop&w=600&q=80"),
        ("dest_singapore", "Gardens by the Bay", "Landmark", "Futuristic Supertree Grove and Flower Dome glass greenhouse.", 1600.0, "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=600&q=80"),
        ("dest_singapore", "Marina Bay Sands SkyPark", "Landmark", "Iconic rooftop infinity pool lookout over Singapore skyline.", 2200.0, "https://images.unsplash.com/photo-1508964942454-1a56651d54ac?auto=format&fit=crop&w=600&q=80"),
        ("dest_singapore", "Sentosa Island Beach Resort", "Relaxation", "Tropical resort island with sandy beaches and sea attractions.", 1000.0, "https://images.unsplash.com/photo-1565967511849-76a4598271ee?auto=format&fit=crop&w=600&q=80"),
        ("dest_ny", "Central Park Meadow", "Nature", "Vast urban park in Manhattan featuring Bethesda Terrace.", 0.0, "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=600&q=80"),
        ("dest_ny", "Empire State Building Observatory", "Landmark", "Historic skyscraper lookout point over New York Harbor.", 3800.0, "https://images.unsplash.com/photo-1534430480872-3498386e7856?auto=format&fit=crop&w=600&q=80"),
        ("dest_ny", "Metropolitan Museum of Art", "Museum", "Comprehensive art collection spanning 5,000 years of history.", 2500.0, "https://images.unsplash.com/photo-1554907984-15263bfd63bd?auto=format&fit=crop&w=600&q=80"),
        ("dest_istanbul", "Hagia Sophia Grand Mosque", "Culture", "Architectural marvel with magnificent Byzantine domes.", 0.0, "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=600&q=80"),
        ("dest_istanbul", "Grand Bazaar Shopping", "Shopping", "Historic covered market with over 4,000 artisan shops.", 0.0, "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=600&q=80"),
        ("dest_istanbul", "Bosphorus Strait Cruise", "Sightseeing", "Scenic ferry cruise between Europe and Asia continents.", 1200.0, "https://images.unsplash.com/photo-1527838832700-54595d2f4586?auto=format&fit=crop&w=600&q=80")
    ]

    for d_id, name, cat, desc, cost, img in seed_places:
        p_id = f"PLC-{uuid.uuid4().hex[:6].upper()}"
        place_item = {
            "id": p_id,
            "destination_id": d_id,
            "name": name,
            "category": cat,
            "description": desc,
            "estimated_cost": cost,
            "image": img
        }
        places_by_id[p_id] = place_item
        places_list.append(place_item)

    seed_packing = [
        ("Essentials", "Passport & Identification", True),
        ("Essentials", "Flight & Hotel Confirmation Slips", True),
        ("Clothing", "Light Cotton Shirts & Trousers", False),
        ("Clothing", "Rain Jacket & Waterproof Shoes", True),
        ("Electronics", "Camera, Spare Batteries & Memory Card", False),
        ("Electronics", "Universal Travel Adapter & Power Bank", True),
        ("Personal", "Sunscreen & Mosquito Repellent Spray", False)
    ]

    for cat, item_name, comp in seed_packing:
        pk_id = f"PCK-{uuid.uuid4().hex[:6].upper()}"
        pack_item = {
            "id": pk_id,
            "trip_id": "TRIP-101",
            "category": cat,
            "name": item_name,
            "completed": comp
        }
        packing_items_by_id[pk_id] = pack_item
        packing_items_list.append(pack_item)

    # Seed Journal entries
    seed_journals = [
        ("TRIP-101", 1, "Arrived in Green Paradise", "Landing in Kochi was effortless. The monsoon breeze over the palm groves immediately made the journey special.", "2026-10-10"),
        ("TRIP-102", 1, "Sunrise at Fushimi Inari", "Walking under thousands of red torii gates as morning mist cleared over Mount Inari was unforgettable.", "2026-09-24")
    ]

    for t_id, day, title, content, date_str in seed_journals:
        j_id = f"JRN-{uuid.uuid4().hex[:6].upper()}"
        journal_item = {
            "id": j_id,
            "trip_id": t_id,
            "day": day,
            "title": title,
            "content": content,
            "date": date_str
        }
        journal_entries_by_id[j_id] = journal_item
        journal_entries_list.append(journal_item)

seed_data()

def find_trip(trip_id):
    return trips_by_id.get(trip_id)

def find_destination(dest_id):
    return destinations_by_id.get(dest_id)

def find_activity(act_id):
    return activities_by_id.get(act_id)

def find_place(place_id):
    return places_by_id.get(place_id)

def find_packing_item(item_id):
    return packing_items_by_id.get(item_id)

def find_journal_entry(entry_id):
    return journal_entries_by_id.get(entry_id)

def success_response(data, status_code=200):
    return jsonify({"success": True, "data": data}), status_code

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code

def calculate_trip_duration(start_date, end_date):
    try:
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")
        delta = (d2 - d1).days + 1
        return max(1, delta)
    except Exception:
        return 1

def calculate_trip_budget(trip_id):
    trip_acts = [a for a in activities_list if a["trip_id"] == trip_id]
    total_est = sum(a["estimated_cost"] for a in trip_acts)
    
    breakdown = {}
    for a in trip_acts:
        cat = a["category"]
        breakdown[cat] = breakdown.get(cat, 0.0) + a["estimated_cost"]

    trip = find_trip(trip_id)
    duration = calculate_trip_duration(trip["start_date"], trip["end_date"]) if trip else 1
    travelers = trip["travelers"] if trip and trip.get("travelers") else 1
    
    per_person = round(total_est / max(1, travelers), 2)
    daily_avg = round(total_est / max(1, duration), 2)
    
    return {
        "total_estimated": round(total_est, 2),
        "per_person": per_person,
        "daily_average": daily_avg,
        "duration_days": duration,
        "travelers": travelers,
        "category_breakdown": breakdown
    }

def calculate_packing_progress(trip_id):
    items = [p for p in packing_items_list if p["trip_id"] == trip_id]
    if not items:
        return {"total": 0, "completed": 0, "remaining": 0, "percentage": 0.0}
    
    comp = sum(1 for i in items if i["completed"])
    tot = len(items)
    pct = round((comp / tot) * 100, 1)
    return {
        "total": tot,
        "completed": comp,
        "remaining": tot - comp,
        "percentage": pct
    }

def calculate_trip_progress(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return 0.0

    score = 20.0  # Base creation
    
    trip_acts = [a for a in activities_list if a["trip_id"] == trip_id]
    if len(trip_acts) >= 3:
        score += 30.0
    elif len(trip_acts) >= 1:
        score += 15.0

    pack_info = calculate_packing_progress(trip_id)
    score += (pack_info["percentage"] * 0.25)

    dest_places = [p for p in places_list if p["destination_id"] == trip["destination_id"]]
    if len(dest_places) >= 1:
        score += 15.0

    j_entries = [j for j in journal_entries_list if j["trip_id"] == trip_id]
    if len(j_entries) >= 1:
        score += 10.0

    return min(100.0, round(score, 1))

def calculate_overall_packing_progress():
    if not packing_items_list:
        return {"total": 0, "completed": 0, "percentage": 0.0}
    comp = sum(1 for i in packing_items_list if i["completed"])
    tot = len(packing_items_list)
    pct = round((comp / tot) * 100, 1)
    return {"total": tot, "completed": comp, "percentage": pct}

def build_trip_summary(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return None

    dest = find_destination(trip["destination_id"])
    acts = [a for a in activities_list if a["trip_id"] == trip_id]
    acts.sort(key=lambda x: (x["day"], x["time"]))

    budget = calculate_trip_budget(trip_id)
    packing_progress = calculate_packing_progress(trip_id)
    packing_items = [p for p in packing_items_list if p["trip_id"] == trip_id]
    places = [p for p in places_list if p["destination_id"] == trip["destination_id"]]
    journals = [j for j in journal_entries_list if j["trip_id"] == trip_id]
    progress = calculate_trip_progress(trip_id)

    return {
        "trip": trip,
        "destination": dest,
        "activities": acts,
        "budget": budget,
        "packing": packing_items,
        "packing_progress": packing_progress,
        "places": places,
        "journal": journals,
        "journal_entries": journals,
        "progress_percentage": progress
    }

def build_dashboard():
    upcoming_trips = [t for t in trips_list if t["status"] in ["Planning", "Upcoming", "In Progress"]]
    upcoming_trips.sort(key=lambda x: x["start_date"])
    
    primary_trip = upcoming_trips[0] if upcoming_trips else (trips_list[0] if trips_list else None)
    summary = build_trip_summary(primary_trip["id"]) if primary_trip else None

    total_calculated_budget = sum(calculate_trip_budget(t["id"])["total_estimated"] for t in trips_list)
    overall_packing = calculate_overall_packing_progress()

    return {
        "total_trips": len(trips_list),
        "upcoming_count": len([t for t in trips_list if t["status"] in ["Planning", "Upcoming", "In Progress"]]),
        "completed_count": len([t for t in trips_list if t["status"] == "Completed"]),
        "destinations_count": len(destinations_list),
        "total_estimated_budget": total_calculated_budget,
        "overall_packing_progress": overall_packing["percentage"],
        "featured_destinations": destinations_list[:6],
        "primary_journey_summary": summary,
        "recent_journeys": trips_list
    }

def validate_trip(data):
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object."
    if not data.get("name") or not isinstance(data.get("name"), str):
        return False, "Journey name is required."
    if not data.get("destination_id") or not isinstance(data.get("destination_id"), str):
        return False, "Destination ID is required."
    if not find_destination(data.get("destination_id")):
        return False, f"Destination ID '{data.get('destination_id')}' not found."
    if not data.get("start_date") or not data.get("end_date"):
        return False, "Start date and end date are required."
    try:
        d1 = datetime.strptime(data["start_date"], "%Y-%m-%d")
        d2 = datetime.strptime(data["end_date"], "%Y-%m-%d")
        if d2 < d1:
            return False, "End date cannot be earlier than start date."
    except ValueError:
        return False, "Invalid date format. Expected YYYY-MM-DD."
    return True, None

def validate_activity(data):
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object."
    if not data.get("title"):
        return False, "Activity title is required."
    try:
        day = int(data.get("day", 1))
        if day < 1:
            return False, "Day must be a positive integer."
    except (ValueError, TypeError):
        return False, "Invalid day number."
    return True, None

@app.route("/api/dashboard", methods=["GET"])
def api_get_dashboard():
    return success_response(build_dashboard())

@app.route("/api/destinations", methods=["GET"])
def api_get_destinations():
    search = request.args.get("search", "").lower().strip()
    style = request.args.get("style", "all")
    region = request.args.get("region", "all")

    filtered = list(destinations_list)

    if style != "all":
        filtered = [d for d in filtered if style in d["travel_styles"]]
    if region != "all":
        filtered = [d for d in filtered if d["region"].lower() == region.lower()]
    if search:
        filtered = [d for d in filtered if search in d["name"].lower() or search in d["country"].lower() or search in d["description"].lower()]

    return success_response(filtered)

@app.route("/api/destinations", methods=["POST"])
def api_create_destination():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("country"):
        return error_response("Destination name and country are required.", 400)

    d_id = f"dest_{uuid.uuid4().hex[:6].lower()}"
    new_dest = {
        "id": d_id,
        "name": data["name"].strip(),
        "country": data["country"].strip(),
        "region": data.get("region", "Global").strip(),
        "description": data.get("description", "").strip(),
        "image": data.get("image", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"),
        "travel_styles": data.get("travel_styles", ["Culture"]),
        "estimated_daily_budget": float(data.get("estimated_daily_budget", 5000.0)),
        "recommended_days": int(data.get("recommended_days", 4))
    }
    destinations_by_id[d_id] = new_dest
    destinations_list.append(new_dest)
    return success_response(new_dest, 201)

@app.route("/api/destinations/<dest_id>", methods=["GET"])
def api_get_destination(dest_id):
    dest = find_destination(dest_id)
    if not dest:
        return error_response(f"Destination '{dest_id}' not found.", 404)
    dest_places = [p for p in places_list if p["destination_id"] == dest_id]
    result = dict(dest)
    result["places"] = dest_places
    return success_response(result)

@app.route("/api/trips", methods=["GET"])
def api_get_trips():
    status = request.args.get("status", "all")
    filtered = list(trips_list)
    if status != "all":
        filtered = [t for t in filtered if t["status"].lower() == status.lower()]
    filtered.sort(key=lambda x: x["start_date"])
    return success_response(filtered)

@app.route("/api/trips/<trip_id>", methods=["GET"])
def api_get_trip(trip_id):
    summary = build_trip_summary(trip_id)
    if not summary:
        return error_response(f"Trip '{trip_id}' not found.", 404)
    return success_response(summary)

@app.route("/api/trips", methods=["POST"])
def api_create_trip():
    data = request.get_json(silent=True)
    is_valid, err = validate_trip(data)
    if not is_valid:
        return error_response(err, 400)

    dest = find_destination(data["destination_id"])
    t_id = f"TRIP-{uuid.uuid4().hex[:6].upper()}"

    new_trip = {
        "id": t_id,
        "name": data["name"].strip(),
        "destination_id": data["destination_id"],
        "destination_name": dest["name"],
        "country": dest["country"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "travelers": int(data.get("travelers", 1)),
        "travel_style": data.get("travel_style", dest["travel_styles"][0] if dest["travel_styles"] else "Explorer"),
        "status": "Planning",
        "created_at": datetime.now().isoformat()
    }

    trips_by_id[t_id] = new_trip
    trips_list.append(new_trip)

    return success_response(build_trip_summary(t_id), 201)

@app.route("/api/trips/<trip_id>", methods=["PATCH"])
def api_update_trip(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return error_response(f"Trip '{trip_id}' not found.", 404)

    data = request.get_json(silent=True) or {}
    if "name" in data:
        trip["name"] = data["name"].strip()
    if "status" in data and data["status"] in ["Planning", "Upcoming", "In Progress", "Completed"]:
        trip["status"] = data["status"]
    if "travelers" in data:
        try:
            trip["travelers"] = max(1, int(data["travelers"]))
        except (ValueError, TypeError):
            pass
    if "travel_style" in data:
        trip["travel_style"] = data["travel_style"]

    return success_response(build_trip_summary(trip_id))

@app.route("/api/trips/<trip_id>", methods=["DELETE"])
def api_delete_trip(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return error_response(f"Trip '{trip_id}' not found.", 404)

    trips_list.remove(trip)
    del trips_by_id[trip_id]
    return success_response({"id": trip_id, "deleted": True})

@app.route("/api/trips/<trip_id>/activities", methods=["GET"])
def api_get_activities(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return error_response(f"Trip '{trip_id}' not found.", 404)
    acts = [a for a in activities_list if a["trip_id"] == trip_id]
    acts.sort(key=lambda x: (x["day"], x["time"]))
    return success_response(acts)

@app.route("/api/trips/<trip_id>/activities", methods=["POST"])
def api_create_activity(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return error_response(f"Trip '{trip_id}' not found.", 404)

    data = request.get_json(silent=True)
    is_valid, err = validate_activity(data)
    if not is_valid:
        return error_response(err, 400)

    a_id = f"ACT-{uuid.uuid4().hex[:6].upper()}"
    new_act = {
        "id": a_id,
        "trip_id": trip_id,
        "day": int(data.get("day", 1)),
        "title": data["title"].strip(),
        "time": data.get("time", "10:00"),
        "location": data.get("location", trip["destination_name"]),
        "category": data.get("category", "Sightseeing"),
        "duration": data.get("duration", "1 hour"),
        "estimated_cost": round(float(data.get("estimated_cost", 0.0)), 2),
        "notes": data.get("notes", "")
    }

    activities_by_id[a_id] = new_act
    activities_list.append(new_act)
    return success_response(new_act, 201)

@app.route("/api/activities/<activity_id>", methods=["PATCH"])
def api_update_activity(activity_id):
    act = find_activity(activity_id)
    if not act:
        return error_response(f"Activity '{activity_id}' not found.", 404)

    data = request.get_json(silent=True) or {}
    if "title" in data:
        act["title"] = data["title"]
    if "day" in data:
        try:
            act["day"] = max(1, int(data["day"]))
        except (ValueError, TypeError):
            pass
    if "time" in data:
        act["time"] = data["time"]
    if "estimated_cost" in data:
        try:
            act["estimated_cost"] = round(float(data["estimated_cost"]), 2)
        except (ValueError, TypeError):
            pass

    return success_response(act)

@app.route("/api/activities/<activity_id>", methods=["DELETE"])
def api_delete_activity(activity_id):
    act = find_activity(activity_id)
    if not act:
        return error_response(f"Activity '{activity_id}' not found.", 404)

    activities_list.remove(act)
    del activities_by_id[activity_id]
    return success_response({"id": activity_id, "deleted": True})

@app.route("/api/places", methods=["GET"])
def api_get_places():
    dest_id = request.args.get("destination_id")
    if dest_id:
        filtered = [p for p in places_list if p["destination_id"] == dest_id]
    else:
        filtered = list(places_list)
    return success_response(filtered)

@app.route("/api/trips/<trip_id>/places", methods=["GET"])
def api_get_trip_places(trip_id):
    trip = find_trip(trip_id)
    if not trip:
        return error_response(f"Trip '{trip_id}' not found.", 404)
    filtered = [p for p in places_list if p["destination_id"] == trip["destination_id"]]
    return success_response(filtered)

@app.route("/api/places", methods=["POST"])
@app.route("/api/places/save", methods=["POST"])
def api_save_place():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("destination_id"):
        return error_response("Place name and destination_id are required.", 400)

    p_id = f"PLC-{uuid.uuid4().hex[:6].upper()}"
    new_place = {
        "id": p_id,
        "destination_id": data["destination_id"],
        "name": data["name"].strip(),
        "category": data.get("category", "Attraction"),
        "description": data.get("description", ""),
        "estimated_cost": round(float(data.get("estimated_cost", 0.0)), 2),
        "image": data.get("image", "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=600&q=80")
    }
    places_by_id[p_id] = new_place
    places_list.append(new_place)
    return success_response(new_place, 201)

@app.route("/api/places/<place_id>", methods=["DELETE"])
def api_delete_place(place_id):
    place = find_place(place_id)
    if not place:
        return error_response(f"Place '{place_id}' not found.", 404)
    places_list.remove(place)
    del places_by_id[place_id]
    return success_response({"id": place_id, "deleted": True})

@app.route("/api/trips/<trip_id>/packing", methods=["GET"])
def api_get_packing(trip_id):
    items = [p for p in packing_items_list if p["trip_id"] == trip_id]
    return success_response(items)

@app.route("/api/trips/<trip_id>/packing", methods=["POST"])
def api_create_packing_item(trip_id):
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return error_response("Item name is required.")

    pk_id = f"PCK-{uuid.uuid4().hex[:6].upper()}"
    new_item = {
        "id": pk_id,
        "trip_id": trip_id,
        "category": data.get("category", "Essentials"),
        "name": data["name"].strip(),
        "completed": False
    }
    packing_items_by_id[pk_id] = new_item
    packing_items_list.append(new_item)
    return success_response(new_item, 201)

@app.route("/api/packing/<item_id>", methods=["PATCH"])
def api_update_packing_item(item_id):
    item = find_packing_item(item_id)
    if not item:
        return error_response(f"Packing item '{item_id}' not found.", 404)

    data = request.get_json(silent=True) or {}
    if "completed" in data:
        item["completed"] = bool(data["completed"])
    if "name" in data:
        item["name"] = data["name"].strip()

    return success_response(item)

@app.route("/api/packing/<item_id>", methods=["DELETE"])
def api_delete_packing_item(item_id):
    item = find_packing_item(item_id)
    if not item:
        return error_response(f"Packing item '{item_id}' not found.", 404)
    packing_items_list.remove(item)
    del packing_items_by_id[item_id]
    return success_response({"id": item_id, "deleted": True})

@app.route("/api/trips/<trip_id>/journal", methods=["GET"])
def api_get_journal(trip_id):
    entries = [j for j in journal_entries_list if j["trip_id"] == trip_id]
    entries.sort(key=lambda x: x["day"])
    return success_response(entries)

@app.route("/api/trips/<trip_id>/journal", methods=["POST"])
def api_create_journal_entry(trip_id):
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("content"):
        return error_response("Journal title and content are required.")

    j_id = f"JRN-{uuid.uuid4().hex[:6].upper()}"
    new_entry = {
        "id": j_id,
        "trip_id": trip_id,
        "day": int(data.get("day", 1)),
        "title": data["title"].strip(),
        "content": data["content"].strip(),
        "date": data.get("date", datetime.now().strftime("%Y-%m-%d"))
    }
    journal_entries_by_id[j_id] = new_entry
    journal_entries_list.append(new_entry)
    return success_response(new_entry, 201)

@app.route("/api/journal/<entry_id>", methods=["DELETE"])
def api_delete_journal_entry(entry_id):
    entry = find_journal_entry(entry_id)
    if not entry:
        return error_response(f"Journal entry '{entry_id}' not found.", 404)
    journal_entries_list.remove(entry)
    del journal_entries_by_id[entry_id]
    return success_response({"id": entry_id, "deleted": True})

@app.route("/api/search", methods=["GET"])
def api_global_search():
    q = request.args.get("q", "").lower().strip()
    if not q:
        return success_response({"destinations": [], "trips": [], "places": [], "activities": []})

    m_dest = [d for d in destinations_list if q in d["name"].lower() or q in d["country"].lower() or q in d["region"].lower()]
    m_trips = [t for t in trips_list if q in t["name"].lower() or q in t["destination_name"].lower()]
    m_places = [p for p in places_list if q in p["name"].lower() or q in p["category"].lower()]
    m_acts = [a for a in activities_list if q in a["title"].lower() or q in a["location"].lower()]

    return success_response({
        "destinations": m_dest[:5],
        "trips": m_trips[:5],
        "places": m_places[:5],
        "activities": m_acts[:5]
    })

@app.route("/")
def page_index():
    return render_template("index.html")

@app.route("/discover")
def page_discover():
    return render_template("discover.html")

@app.route("/trips")
def page_trips():
    return render_template("trips.html")

@app.route("/itinerary")
def page_itinerary():
    return render_template("itinerary.html")

@app.route("/places")
def page_places():
    return render_template("places.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
