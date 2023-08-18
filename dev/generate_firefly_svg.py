import random
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring

import numpy as np

# Seed for reproducibility
random.seed(0)
np.random.seed(0)

# Constants
NUM_FIREFLIES = 300
SVG_WIDTH = 1920
SVG_HEIGHT = 1080


def generate_firefly_full_circle():
    h = random.randint(50, SVG_WIDTH - 50)
    k = random.randint(50, SVG_HEIGHT - 50)
    r_firefly = random.uniform(4, 12)
    r_motion = random.randint(30, 150)
    omega = random.uniform(0.05, 0.25)
    duration = 2 * np.pi / omega
    start_angle = random.uniform(0, 2 * np.pi)
    start_x = h + r_motion * np.cos(start_angle)
    start_y = k + r_motion * np.sin(start_angle)
    noise_level = random.uniform(0, 3)

    # Round to 2 decimal places (decreases file size)
    r_firefly = round(r_firefly, 1)
    duration = round(duration, 1)
    start_x = round(start_x, 1)
    start_y = round(start_y, 1)

    return start_x, start_y, h, k, r_firefly, r_motion, omega, duration, noise_level


svg = Element(
    "svg",
    width=str(SVG_WIDTH),
    height=str(SVG_HEIGHT),
    xmlns="http://www.w3.org/2000/svg",
)
defs = SubElement(svg, "defs")

linear_gradient = SubElement(
    defs, "linearGradient", id="backgroundGradient", gradientTransform="rotate(60)"
)
SubElement(
    linear_gradient,
    "stop",
    offset="0%",
    style="stop-color:#fea75f; stop-opacity:0.2",
)
SubElement(
    linear_gradient,
    "stop",
    offset="100%",
    style="stop-color:#294275; stop-opacity:0.2",
)
background = SubElement(
    svg,
    "rect",
    x="0",
    y="0",
    width=str(SVG_WIDTH),
    height=str(SVG_HEIGHT),
    fill="url(#backgroundGradient)",
)

firefly_colors = ["#fd7e14", "#014bd1"]
firefly_color_weights = [0.85, 0.15]
for i, color in enumerate(firefly_colors):
    radial_gradient = SubElement(defs, "radialGradient", id=f"fireflyGlow_{i}")
    SubElement(
        radial_gradient,
        "stop",
        offset="0%",
        style=f"stop-color:{color}; stop-opacity:1",
    )
    SubElement(
        radial_gradient,
        "stop",
        offset="100%",
        style=f"stop-color:{color}; stop-opacity:0",
    )

for i in range(NUM_FIREFLIES):
    (
        start_x,
        start_y,
        h,
        k,
        r_firefly,
        r_motion,
        omega,
        duration,
        noise_level,
    ) = generate_firefly_full_circle()

    # Varying durations for animation
    movement_duration = random.uniform(1.5 * duration, 1.9 * duration)
    movement_duration = round(movement_duration, 2)

    # Create a path for the firefly to follow
    path_data = f"M {start_x},{start_y}"
    for angle in np.linspace(0, 2 * np.pi, num=50):
        x = h + r_motion * np.cos(angle) + noise_level * np.sin(10 * angle)
        y = k + r_motion * np.sin(angle) + noise_level * np.cos(10 * angle)
        x = round(x, 1)
        y = round(y, 1)
        path_data += f" L {x},{y}"
    path_data += f" Z"

    # Firefly
    firefly_fill = random.choices(
        population=range(len(firefly_colors)), weights=firefly_color_weights
    )[0]
    firefly = SubElement(
        svg,
        "circle",
        cx=str(start_x),
        cy=str(start_y),
        r=str(r_firefly),
        fill=f"url(#fireflyGlow_{firefly_fill})",
    )

    path_id = f"path_{i}"
    path = SubElement(svg, "path", id=path_id, d=path_data, fill="none")

    animate_motion = SubElement(
        firefly, "animateMotion", dur=f"{movement_duration}s", repeatCount="indefinite"
    )
    SubElement(animate_motion, "mpath", href=f"#{path_id}")

    glow_duration = np.random.normal(6, 2)
    glow_duration = max(4, glow_duration)
    glow_duration = min(8, glow_duration)
    glow_duration = round(glow_duration, 1)
    SubElement(
        firefly,
        "animate",
        attributeName="opacity",
        values="0.2;1;0.4;1;0.6;1;0.8;0.2",
        dur=f"{glow_duration}s",
        repeatCount="indefinite",
    )

# Convert to a nicely formatted string
dom = parseString(tostring(svg))
svg_str_with_paths = dom.toprettyxml()

with open("firefly.svg", "w") as f:
    f.write(svg_str_with_paths)
