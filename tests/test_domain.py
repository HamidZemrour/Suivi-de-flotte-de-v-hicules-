import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from domain import haversine, validate, incidents
class DomainTests(unittest.TestCase):
    def test_distance(self):
        self.assertAlmostEqual(haversine(0,0,0,1),111.195,places=2)
        self.assertEqual(haversine(33,-7,33,-7),0)
    def test_quality(self):
        e=dict(event_id='a',vehicle_id='V1',event_ms=1,latitude=33.58,longitude=-7.6,speed_kmh=80)
        self.assertTrue(validate(e)); self.assertFalse(incidents(e)['speeding'])
        e['speed_kmh']=81; self.assertTrue(incidents(e)['speeding'])
        e['latitude']=34; self.assertTrue(incidents(e)['outside_zone'])
        e['latitude']=91; self.assertFalse(validate(e))
        self.assertFalse(validate({}))
if __name__=='__main__': unittest.main()
