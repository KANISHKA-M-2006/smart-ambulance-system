import cv2
import folium
import math

# 📍 Locations (Chennai)
current_location = (13.0827, 80.2707)
hospital_location = (13.0674, 80.2376)

# 📏 Distance calculation
def calculate_distance(loc1, loc2):
    return round(math.sqrt(
        (loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2
    ) * 111, 2)

distance = calculate_distance(current_location, hospital_location)

# 🗺️ Create map
my_map = folium.Map(location=current_location, zoom_start=14)

# 🏷️ Add Title
title_html = '''
<h3 align="center" style="font-size:22px"><b>🚑 Smart Ambulance Priority and Crowd Aware - Navigation System</b></h3>
'''
my_map.get_root().html.add_child(folium.Element(title_html))

# 🎥 Open camera
cap = cv2.VideoCapture(0)

crowd_detected = False

print("\n🚀 SYSTEM STARTED")
print("Press 'A' for ambulance alert")
print("Press 'ESC' to exit\n")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Camera not working!")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crowd detection
    avg_brightness = gray.mean()

    if avg_brightness < 200:
        status = "CROWD DETECTED"
        color = (0, 0, 255)
        crowd_detected = True
    else:
        status = "NO CROWD"
        color = (0, 255, 0)

    # Display on camera
    cv2.putText(frame, status, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Live Crowd Detection", frame)

    key = cv2.waitKey(1)

    # 🚑 Ambulance simulation
    if key == ord('a'):
        print("\n🚑 AMBULANCE ACTIVATED!")
        print(f"📍 Nearest Hospital Distance: {distance} km")
        print("🛣️ Finding shortest route...")
        print("📢 Public Alert: Please clear the road!")
        print("⏱️ Estimated Time Saved: 5–10 minutes")
        print("🔊 Smart Route Generated Successfully!\n")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

# 🔴 Crowd Area
if crowd_detected:
    folium.Circle(
        location=current_location,
        radius=300,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(my_map)

    folium.Marker(
        current_location,
        popup="🚨 Crowd Area (High Traffic)",
        icon=folium.Icon(color='red')
    ).add_to(my_map)

else:
    folium.Circle(
        location=current_location,
        radius=200,
        color='green',
        fill=True,
        fill_color='green'
    ).add_to(my_map)

    folium.Marker(
        current_location,
        popup="✅ Clear Area",
        icon=folium.Icon(color='green')
    ).add_to(my_map)

# 🏥 Hospital
folium.Marker(
    hospital_location,
    popup=f"🏥 Nearest Hospital ({distance} km)",
    icon=folium.Icon(color='blue')
).add_to(my_map)

# 🛣️ Route Line
folium.PolyLine(
    locations=[current_location, hospital_location],
    color='blue',
    weight=5
).add_to(my_map)

# 💾 Save map
my_map.save("final_map.html")

print("✅ SYSTEM COMPLETED SUCCESSFULLY!")
print("👉 Open final_map.html to view result")