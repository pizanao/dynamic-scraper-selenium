from app.models import ScrapedRecord

def test_record_validates():
    r = ScrapedRecord(external_id='ITEM-001', title='Workforce Signal', category='HR', price=1, rating=4, url='/x')
    assert r.category == 'HR'
