from ..rt import Color
from ..rt import Point
from ..rt import PointLight

def test_a_point_light_has_a_position_and_intensity():
    intensity = Color(1, 1, 1)
    position = Point(0, 0, 0)
    light = PointLight(position, intensity)
    
    assert intensity == light.intensity
    assert position == light.position