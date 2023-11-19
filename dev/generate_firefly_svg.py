import random
import xml.etree.ElementTree as ET
from typing import Optional
from xml.etree.ElementTree import Element, SubElement

import numpy as np

# Seed for reproducibility
random.seed(100)
np.random.seed(100)

# Constants (wide)
# FILE_NAME = "../content/assets/images/moving-firefly-wide.svg"
# NUM_FIREFLIES = 60
# SVG_WIDTH = 1920
# SVG_HEIGHT = 1080
# MIN_FIREFLY_RADIUS = 4
# MAX_FIREFLY_RADIUS = 13

# Constants (tall)
FILE_NAME = "../content/assets/images/moving-firefly-tall.svg"
NUM_FIREFLIES = 30
SVG_WIDTH = 1080
SVG_HEIGHT = 1920
MIN_FIREFLY_RADIUS = 10
MAX_FIREFLY_RADIUS = 15

# Safe area
SAFE_AREA_X = 1
SAFE_AREA_Y = 1


def gen_firefly():
    """
    Generate parameters for a firefly.

    Returns:
        Tuple[float, int, int, float]: Radius, center x, center y, motion radius.
    """
    firefly_r = np.random.uniform(MIN_FIREFLY_RADIUS, MAX_FIREFLY_RADIUS)
    motion_cx = np.random.randint(SAFE_AREA_X, SVG_WIDTH - SAFE_AREA_X)
    motion_cy = np.random.randint(SAFE_AREA_Y, SVG_HEIGHT - SAFE_AREA_Y)
    motion_r = np.random.randint(50, 300)
    return (
        round(firefly_r, 1),
        motion_cx,
        motion_cy,
        round(motion_r, 1),
    )


def is_counterclockwise(x1, y1, x2, y2, x3, y3) -> bool:
    """
    Check if three points make a counterclockwise turn.

    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.
        x3, y3: Coordinates of the third point.

    Returns:
        bool: True if the points are in counterclockwise order, False otherwise.
    """
    return (y3 - y1) * (x2 - x1) > (y2 - y1) * (x3 - x1)


def line_intersects_line(Ax, Ay, Bx, By, Cx, Cy, Dx, Dy) -> bool:
    """
    Check if two line segments intersect.

    Args:
        Ax, Ay: Starting point of the first line segment.
        Bx, By: Ending point of the first line segment.
        Cx, Cy: Starting point of the second line segment.
        Dx, Dy: Ending point of the second line segment.

    Returns:
        bool: True if the line segments intersect, False otherwise.
    """
    return is_counterclockwise(Ax, Ay, Cx, Cy, Dx, Dy) != is_counterclockwise(
        Bx, By, Cx, Cy, Dx, Dy
    ) and is_counterclockwise(Ax, Ay, Bx, By, Cx, Cy) != is_counterclockwise(
        Ax, Ay, Bx, By, Dx, Dy
    )


def line_intersects_rect(x1, y1, x2, y2, rx1, ry1, rx2, ry2) -> bool:
    """
    Check if a line segment intersects with a rectangle.

    Args:
        x1, y1: Starting point of the line segment.
        x2, y2: Ending point of the line segment.
        rx1, ry1: Top-left corner of the rectangle.
        rx2, ry2: Bottom-right corner of the rectangle.

    Returns:
        bool: True if the line segment intersects the rectangle, False otherwise.
    """
    return (
        line_intersects_line(x1, y1, x2, y2, rx1, ry1, rx1, ry2)  # Left side
        or line_intersects_line(x1, y1, x2, y2, rx1, ry1, rx2, ry1)  # Top side
        or line_intersects_line(x1, y1, x2, y2, rx1, ry2, rx2, ry2)  # Bottom side
        or line_intersects_line(x1, y1, x2, y2, rx2, ry1, rx2, ry2)  # Right side
    )


def gen_firefly_path(motion_cx, motion_cy, motion_r) -> Optional[str]:
    """
    Generate a path for a firefly to follow.

    Args:
        motion_cx: Center x of the motion.
        motion_cy: Center y of the motion.
        motion_r: Radius of the motion.

    Returns:
        Optional[str]: SVG path data if the path is valid, None otherwise.
    """
    start_angle = np.random.uniform(0, 2 * np.pi)
    path_data = ""

    motion_direction = np.random.choice([-1, 1])
    motion_a = motion_r * np.random.uniform(1, 2)
    motion_b = motion_r * np.random.uniform(0.5, 1.5)

    path_data = ""
    angle = start_angle
    last_x, last_y = None, None
    for angle in np.linspace(
        start_angle, start_angle + motion_direction * 2 * np.pi, 50
    ):
        # Dynamic changes in radii for more randomness
        # motion_a = motion_r * np.random.uniform(1.0, 2.2)
        # motion_b = motion_r * np.random.uniform(0.5, 1.7)

        x = motion_cx + motion_a * np.cos(angle)
        y = motion_cy + motion_b * np.sin(angle)

        if angle == start_angle:
            path_data += f"M {round(x, 1)},{round(y, 1)}"
        else:
            x += motion_r * np.random.uniform(-0.25, 0.3)
            y += motion_r * np.random.uniform(-0.25, 0.3)
            path_data += f" L {round(x, 1)},{round(y, 1)}"

        # Check if the path is outside the safe area
        if (
            x < SAFE_AREA_X
            or x > SVG_WIDTH - SAFE_AREA_X
            or y < SAFE_AREA_Y
            or y > SVG_HEIGHT - SAFE_AREA_Y
        ):
            return None

        # Check if the path from the last point to the current point intersects the 100x100 area
        # at the center of the screen,
        if last_x is not None and line_intersects_rect(
            x1=last_x,
            y1=last_y,
            x2=x,
            y2=y,
            rx1=SVG_WIDTH / 2 - 100,
            ry1=SVG_HEIGHT / 2 - 100,
            rx2=SVG_WIDTH / 2 + 100,
            ry2=SVG_HEIGHT / 2 + 100,
        ):
            return None

        last_x, last_y = x, y

    path_data += f" Z"
    return path_data


svg = Element(
    "svg",
    {
        "width": str(SVG_WIDTH),
        "height": str(SVG_HEIGHT),
        "version": "1.1",
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
    },
)
defs = SubElement(svg, "defs")

# Background gradient
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

# Firefly glow gradients
firefly_colors = ["#fd7e14", "#014bd1"]
firefly_color_weights = [0.8, 0.2]
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

# Fireflies
current_firefly = 0
while current_firefly < NUM_FIREFLIES:
    firefly_r, motion_cx, motion_cy, motion_r = gen_firefly()

    # Varying durations for animation
    angular_velocity = np.random.uniform(0.015, 0.020)
    circuit_duration = 2 * np.pi / angular_velocity
    circuit_duration = round(circuit_duration, 2)

    # Create a path for the firefly to follow
    path_data = gen_firefly_path(motion_cx, motion_cy, motion_r)
    if path_data is None:
        continue

    # Create the firefly
    firefly_fill = np.random.choice(
        a=range(len(firefly_colors)), p=firefly_color_weights
    )
    firefly = SubElement(
        svg,
        "circle",
        r=str(firefly_r),
        fill=f"url(#fireflyGlow_{firefly_fill})",
    )

    # Create the path for the firefly to follow
    path_id = f"path_{current_firefly}"
    path = SubElement(
        svg,
        "path",
        {
            "id": path_id,
            "d": path_data,
            "fill": "none",
            "stroke": "none",
            # "stroke": "rgba(0,0,0,0.5)",
            # "stroke-width": "0.5",
        },
    )

    # Animate the firefly along the path
    animate_motion = SubElement(
        firefly,
        "animateMotion",
        path=path_data,
        dur=f"{circuit_duration}s",
        repeatCount="indefinite",
    )
    SubElement(
        animate_motion,
        "mpath",
        {
            "xlink:href": f"#{path_id}",
        },
    )

    # DEBUG: firefly number label
    # firefly_number = SubElement(
    #    svg,
    #    "text",
    # )
    # firefly_number.text = str(current_firefly)
    # animate_motion_text = SubElement(
    #    firefly_number,
    #    "animateMotion",
    #    path=path_data,
    #    dur=f"{circuit_duration}s",
    #    repeatCount="indefinite",
    # )
    # SubElement(
    #    animate_motion_text,
    #    "mpath",
    #    {
    #        "xlink:href": f"#{path_id}",
    #    },
    # )

    # Animate the glow of the firefly
    glow_duration = np.random.uniform(4, 7)
    glow_duration = round(glow_duration, 1)
    animate_glow = SubElement(
        firefly,
        "animate",
        attributeName="opacity",
        values="0.3;1;0.5;1;0.4;1;0.7;0.3",
        dur=f"{glow_duration}s",
        repeatCount="indefinite",
    )

    current_firefly += 1

# Indent the XML
ET.indent(svg, space="  ")

# Convert to a nicely formatted string
svg_string = ET.tostring(svg, encoding="unicode")

with open(FILE_NAME, "w") as f:
    f.write(svg_string)
