import json
from datetime import datetime
from PIL import Image, ImageDraw

# Load route
with open("engine/route.json", "r") as f:
    route = json.load(f)

# Load steps
with open("steps.json", "r") as f:
    steps_data = json.load(f)

# Convert steps to miles
# (Average stride length ~ 0.762m → 0.000473 miles per step)
MILES_PER_STEP = 0.000473

total_steps = sum(entry["steps"] for entry in steps_data)
total_miles = total_steps * MILES_PER_STEP

# Find current position on route
distance_remaining = total_miles
current_point = route[0]

for point in route:
    if distance_remaining >= point["distance_from_start"]:
        current_point = point
    else:
        break

# -----------------------------
# Generate MAP IMAGE
# -----------------------------

# Create a simple map placeholder (800x400)
img = Image.new("RGB", (800, 400), color=(240, 235, 220))
draw = ImageDraw.Draw(img)

# Title
draw.text((20, 20), "Middle-earth Journey", fill="black")

# Draw progress bar
bar_x = 20
bar_y = 80
bar_width = 760
bar_height = 40

progress = min(total_miles / route[-1]["distance_from_start"], 1.0)
progress_width = int(bar_width * progress)

draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline="black")
draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height], fill="green")

# Label
draw.text((20, 140), f"Total steps: {total_steps}", fill="black")
draw.text((20, 170), f"Distance: {total_miles:.2f} miles", fill="black")
draw.text((20, 200), f"Current location: {current_point['name']}", fill="black")

# Save map
img.save("docs/map.png")

# -----------------------------
# Generate JOURNAL
# -----------------------------

journal_text = f"""# Middle-earth Journey Journal

**Date:** {datetime.now().strftime('%Y-%m-%d')}

You have walked **{total_steps} steps**, covering **{total_miles:.2f} miles**.

You are currently at:

### **{current_point['name']}**

{current_point.get('description', '')}

Your journey continues toward Rivendell…
"""

with open("docs/journal.md", "w") as f:
    f.write(journal_text)

print("Map saved to docs/map.png")
print("Journal saved to docs/journal.md")
