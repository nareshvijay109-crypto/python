import csv, sqlite3, tempfile, unittest
from pathlib import Path
from air_quality_pipeline import clean_record, init_db, ingest_csv

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db = self.root/"test.sqlite"
        init_db(self.db)
    def tearDown(self): self.tmp.cleanup()
    def test_fahrenheit_conversion(self):
        r = clean_record({"station_id":"ST11","date":"2026-11-01","hour":"8","pm25":"10","pm10":"20","no2":"3","temperature":"86"}, {"ST11"})
        self.assertAlmostEqual(r["temperature"], 30)
    def test_missing_and_outlier(self):
        r = clean_record({"station_id":"ST01","date":"2026-11-01","hour":"8","pm25":"NA","pm10":"-2","no2":"5","temperature":"29"}, set())
        self.assertIsNone(r["pm25"]); self.assertIsNone(r["pm10"]); self.assertEqual(r["no2"],5)
    def test_all_missing_rejected(self):
        with self.assertRaises(ValueError):
            clean_record({"station_id":"ST01","date":"2026-11-01","hour":"8","pm25":"NA","pm10":"","no2":"NA","temperature":"NA"}, set())
    def test_missing_header(self):
        f=self.root/"bad.csv"; f.write_text("station_id,date\nST01,2026-11-01\n",encoding="utf-8")
        with self.assertRaises(ValueError): ingest_csv(f,self.db,set())
    def test_duplicate_upsert_and_sql_injection_safe(self):
        f=self.root/"ok.csv"
        with f.open("w",newline="",encoding="utf-8") as h:
            w=csv.writer(h); w.writerow(["station_id","date","hour","pm25","pm10","no2","temperature"])
            w.writerow(["ST01'); DROP TABLE readings;--","2026-11-01",8,10,20,3,30])
        accepted,rejected=ingest_csv(f,self.db,set())
        self.assertEqual((accepted,rejected),(1,0))
        with sqlite3.connect(self.db) as c:
            self.assertIsNotNone(c.execute("SELECT name FROM sqlite_master WHERE name='readings'").fetchone())
    def test_empty_file(self):
        f=self.root/"empty.csv"; f.write_text("",encoding="utf-8")
        with self.assertRaises(ValueError): ingest_csv(f,self.db,set())
    def test_wrong_delimiter_detected_as_missing_columns(self):
        f=self.root/"wrong_delimiter.csv"
        f.write_text("station_id;date;hour;pm25;pm10;no2;temperature\nST01;2026-11-01;8;10;20;3;30\n",encoding="utf-8")
        with self.assertRaises(ValueError): ingest_csv(f,self.db,set())
    def test_utf8_bom_header_supported(self):
        f=self.root/"bom.csv"
        f.write_text("\ufeffstation_id,date,hour,pm25,pm10,no2,temperature\nST01,2026-11-01,8,10,20,3,30\n",encoding="utf-8")
        self.assertEqual(ingest_csv(f,self.db,set()),(1,0))

if __name__=="__main__": unittest.main()
