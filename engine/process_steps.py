print("USING NEW COORDINATES")
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
# -----------------------------
location_coords = {
    "Hobbiton": (118, 160),
    "Bywater": (132, 165),
    "Green Hill Country": (145, 175),
    "Tookland": (165, 190),
    "Bree": (260, 175),
    "Midgewater Marshes": (305, 170),
    "Weathertop": (335, 165),
    "Last Bridge": (385, 160),
    "Rivendell": (430, 155)
}


marker_x, marker_y = location_coords.get(current_point["name"], (400, 200))

# -----------------------------
# Build combined canvas
# -----------------------------

# Load and resize map
map_img = Image.open("docs/base_map.png").convert("RGB")
map_img = map_img.resize((800, 400))

# Create final canvas (map + stats area)
final_img = Image.new("RGB", (800, 540), (255, 255, 255))
final_img.paste(map_img, (0, 0))

draw = ImageDraw.Draw(final_img)

# -----------------------------
# Draw marker on map
# -----------------------------

r = 6
draw.ellipse(
    (marker_x - r, marker_y - r, marker_x + r, marker_y + r),
    fill="red",
    outline="black"
)

draw.text((marker_x + 10, marker_y - 10), current_point["name"], fill="black")

# -----------------------------
# Stats + progress bar area
# -----------------------------

stats_top = 410

draw.text((10, stats_top), f"Total steps: {total_steps}", fill="black")
draw.text((10, stats_top + 20), f"Distance: {miles_done:.2f} miles", fill="black")
draw.text((10, stats_top + 40), f"Current location: {current_point['name']}", fill="black")

# Progress bar
bar_left = 10
bar_top = stats_top + 70
bar_width = 780
bar_height = 30

progress = miles_done / total_miles
progress = max(0, min(1, progress))
progress_width = bar_width * progress

draw.rectangle([bar_left, bar_top, bar_left + bar_width, bar_top + bar_height], outline="black")
draw.rectangle([bar_left, bar_top, bar_left + progress_width, bar_top + bar_height], fill="green")

# -----------------------------
# Save final image
# -----------------------------

final_img.save("docs/map.png")

print("Map and journal updated successfully.")
