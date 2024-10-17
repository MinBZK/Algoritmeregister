from app.util import upc


#  test find_new_upc
def test_find_new_upc():
    """Tests the find_new_upc function."""

    new_upc = upc.find_new_upc([])
    assert len(str(new_upc)) == 8


def test_validate_upc():
    """Tests the validate_upc function."""

    new_upc = upc.find_new_upc(avoid_upc_list=[])
    assert upc.validate_upc(new_upc)

    if new_upc[-1] != 9:
        wrong_upc = str(int(new_upc) + 1)
    else:
        wrong_upc = str(int(new_upc) - 1)
    assert not upc.validate_upc(wrong_upc)
    assert not upc.validate_upc("test")
    assert not upc.validate_upc("000")
