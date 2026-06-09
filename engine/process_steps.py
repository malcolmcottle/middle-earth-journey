import json
from PIL import Image, ImageDraw

# -----------------------------
# Load route and steps
# -----------------------------

with open("engine/route.json", "r") as f:
    route = json.load(f)

with open("steps.json", "r") as f:
    steps_data = json.load(f)

# Total steps
total_steps = sum(entry["steps"] for entry in steps_data)

# Convert steps to miles (0.000473 miles per step)
miles_done = total_steps * 0.000473

# -----------------------------
# Determine current location
# -----------------------------

current_point = route[0]
next_point = None

for point in route:
    if miles_done >= point["distance_from_start"]:
        current_point = point
    else:
        next_point = point
        break

total_miles = route[-1]["distance_from_start"]

# -----------------------------
# Generate journal
# -----------------------------

journal_lines = []
journal_lines.append("# Middle-earth Journey\n")
journal_lines.append(f"**Total steps:** {total_steps}")
journal_lines.append(f"**Distance travelled:** {miles_done:.2f} miles")
journal_lines.append(f"**Current location:** {current_point['name']}")

if next_point:
    remaining = next_point["distance_from_start"] - miles_done
    journal_lines.append(f"**Next milestone:** {next_point['name']} ({remaining:.2f} miles to go)")
else:
    journal_lines.append("**You have reached Rivendell!**")

with open("docs/journal.md", "w") as f:
    f.write("\n".join(journal_lines))

# -----------------------------
# Map coordinates per location
# (for your 800x400 resized map)
# -----------------------------

location_coords = {
    "Hobbiton": (120, 220),
    "Bywater": (135, 222),
    "Green Hill Country": (155, 228),
    "Tookland": (170, 235),
    "Bree": (260, 220),
    "Midgewater Marshes": (305, 212),
    "Weathertop": (335, 208),
    "Last Bridge": (385, 202),
    "Rivendell": (430, 195),
}

# Fallback if a name isn't in the dict
marker_x, marker_y = location_coords.get(current_point["name"], (400, 200))

# -----------------------------
# Generate map image
# -----------------------------

base_map = Image.open("docs/base_map.png").convert("RGB")
base_map = base_map.resize((800, 400))

draw = ImageDraw.Draw(base_map)

# Title
draw.text((10, 20), "Middle-earth Journey", fill="black")

# Progress bar
bar_left = 10
bar_top = 330
bar_width = 780
bar_height = 30

progress = miles_done / total_miles if total_miles > 0 else 0
progress = max(0, min(1, progress))  # clamp 0–1
progress_width = bar_width * progress

draw.rectangle(
    [bar_left, bar_top, bar_left + bar_width, bar_top + bar_height],
    outline="black"
)
draw.rectangle(
    [bar_left, bar_top, bar_left + progress_width, bar_top + bar_height],
    fill="green"
)

# Labels
draw.text((10, 280), f"Total steps: {total_steps}", fill="black")
draw.text((10, 300), f"Distance: {miles_done:.2f} miles", fill="black")
draw.text((10, 320), f"Current location: {current_point['name']}", fill="black")

# Current location marker (red dot)
r = 6
draw.ellipse(
    (marker_x - r, marker_y - r, marker_x + r, marker_y + r),
    fill="red",
    outline="black"
)

# Optional: label next to marker
draw.text((marker_x + 8, marker_y - 10), current_point["name"], fill="black")

# Save final map
base_map.save("docs/map.png")

print("Map and journal updated successfully.")
