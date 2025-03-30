from schemas import FontData

def test_font_data_str():
    font = FontData(
        family="Courier New",
        size=16,
        weight=400,
        style="normal"
    )
    expected = "font-family:Courier New;font-size:16px;font-weight:400;font-style:normal"
    assert str(font) == expected