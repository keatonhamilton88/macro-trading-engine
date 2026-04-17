def test_shapes():
    # 1. Check if sensors returned 23+ columns
    assert sensors.shape[1] >= 23
    # 2. Check if forces returned exactly 6 columns
    assert forces.shape[1] == 6
    # 3. Check if PCA returned 3 components
    assert pc_df.shape[1] == 3
