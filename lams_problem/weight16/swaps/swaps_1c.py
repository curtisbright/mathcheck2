if not remove_blocks:
    rowswap[1] = [1, 2, 0, 3, 5, 7, 6, 4, 52, 51, 50, 36, 27, 8, 55, 54, 53, 63, 64, 62, 19, 28, 10, 66, 67, 65, 57, 58, 56, 18, 37, 9, 60, 61, 59, 44, 46, 45, 17, 35, 26, 47, 49, 48, 39, 30, 11, 73, 72, 71, 22, 31, 13, 78, 79, 77, 21, 40, 12, 75, 76, 74, 20, 38, 29, 68, 70, 69, 25, 24, 23, 42, 43, 41, 33, 34, 32, 14, 16, 15]
    colswap[1] = [5, 7, 6, 4, 9, 11, 10, 8, 1, 3, 2, 0, 13, 15, 14, 12, 16, 17, 29, 26, 28, 27, 25, 24, 32, 31, 35, 34, 33, 30, 21, 23, 19, 22, 20, 18, 39, 37, 40, 41, 36, 38, 50, 52, 49, 48, 51, 53, 60, 64, 65, 62, 61, 63, 58, 55, 54, 59, 57, 56]
    rowswap[2] = [2, 1, 0, 3, 4, 5, 6, 7, 50, 56, 62, 20, 29, 38, 68, 69, 70, 44, 57, 63, 11, 30, 39, 71, 72, 73, 45, 51, 64, 12, 21, 40, 74, 75, 76, 46, 52, 58, 13, 22, 31, 77, 78, 79, 17, 26, 35, 47, 48, 49, 8, 27, 36, 53, 54, 55, 9, 18, 37, 59, 60, 61, 10, 19, 28, 65, 66, 67, 14, 15, 16, 23, 24, 25, 32, 33, 34, 41, 42, 43]
    colswap[2] = [8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 16, 17, 33, 32, 31, 30, 34, 35, 27, 29, 26, 28, 24, 25, 21, 19, 18, 20, 22, 23, 36, 40, 41, 37, 38, 39, 46, 45, 44, 47, 43, 42, 48, 49, 51, 53, 50, 52, 59, 56, 57, 54, 58, 55]
rowswap[3] = [3, 2, 0, 1, 5, 7, 6, 4, 78, 75, 68, 42, 33, 14, 66, 60, 47, 73, 76, 70, 25, 34, 16, 55, 61, 49, 72, 79, 69, 24, 43, 15, 54, 67, 48, 71, 77, 74, 23, 41, 32, 53, 65, 59, 39, 30, 11, 63, 57, 44, 22, 31, 13, 52, 58, 46, 21, 40, 12, 51, 64, 45, 20, 38, 29, 50, 62, 56, 19, 18, 17, 36, 37, 35, 27, 28, 26, 8, 10, 9]
colswap[3] = [13, 15, 14, 12, 9, 11, 10, 8, 1, 3, 2, 0, 5, 7, 6, 4, 16, 17, 39, 41, 37, 40, 38, 36, 35, 33, 34, 30, 32, 31, 23, 21, 20, 18, 19, 22, 29, 25, 26, 24, 27, 28, 52, 53, 50, 49, 51, 48, 64, 65, 60, 61, 62, 63, 59, 54, 58, 56, 57, 55]
rowswap[4] = [4, 5, 6, 7, 3, 1, 2, 0, 53, 71, 23, 59, 74, 32, 65, 77, 41, 47, 44, 17, 48, 45, 26, 49, 46, 35, 68, 50, 20, 69, 56, 29, 70, 62, 38, 14, 8, 11, 15, 9, 12, 16, 10, 13, 60, 75, 33, 66, 78, 42, 54, 51, 27, 55, 52, 36, 72, 57, 30, 73, 63, 39, 24, 18, 21, 25, 19, 22, 67, 79, 43, 61, 58, 37, 76, 64, 40, 34, 28, 31]
colswap[4] = [12, 4, 8, 0, 13, 5, 9, 1, 14, 6, 10, 2, 15, 7, 11, 3, 17, 16, 43, 46, 42, 47, 44, 45, 51, 50, 52, 48, 53, 49, 55, 58, 59, 54, 56, 57, 64, 63, 62, 65, 60, 61, 40, 38, 39, 37, 36, 41, 26, 28, 27, 24, 25, 29, 34, 30, 32, 31, 35, 33]
rowswap[5] = [5, 7, 6, 4, 0, 1, 2, 3, 19, 22, 25, 18, 21, 24, 17, 20, 23, 36, 52, 55, 27, 51, 54, 8, 50, 53, 39, 63, 73, 30, 57, 72, 11, 44, 71, 42, 66, 78, 33, 60, 75, 14, 47, 68, 37, 40, 43, 35, 38, 41, 28, 64, 67, 10, 62, 65, 31, 58, 79, 13, 46, 77, 34, 61, 76, 16, 49, 70, 26, 29, 32, 9, 56, 59, 12, 45, 74, 15, 48, 69]
colswap[5] = [1, 5, 9, 13, 3, 7, 11, 15, 2, 6, 10, 14, 0, 4, 8, 12, 17, 16, 49, 52, 48, 51, 53, 50, 60, 64, 61, 65, 63, 62, 55, 57, 56, 54, 58, 59, 46, 43, 45, 47, 44, 42, 22, 18, 23, 19, 21, 20, 25, 29, 27, 26, 24, 28, 35, 32, 30, 34, 33, 31]
rowswap[6] = [6, 7, 4, 5, 3, 0, 2, 1, 43, 79, 67, 15, 69, 48, 24, 72, 54, 34, 31, 28, 32, 29, 26, 33, 30, 27, 76, 40, 64, 74, 12, 45, 75, 21, 51, 61, 37, 58, 59, 9, 56, 60, 18, 57, 16, 70, 49, 25, 73, 55, 41, 38, 35, 42, 39, 36, 77, 13, 46, 78, 22, 52, 65, 10, 62, 66, 19, 63, 23, 71, 53, 14, 11, 8, 68, 20, 50, 47, 17, 44]
colswap[6] = [14, 2, 10, 6, 15, 3, 11, 7, 12, 0, 8, 4, 13, 1, 9, 5, 17, 16, 56, 59, 58, 55, 57, 54, 62, 63, 60, 65, 64, 61, 46, 42, 47, 45, 44, 43, 48, 51, 49, 50, 53, 52, 40, 38, 37, 41, 39, 36, 20, 22, 18, 23, 21, 19, 33, 32, 31, 30, 35, 34]
rowswap[7] = [7, 6, 4, 5, 2, 0, 1, 3, 31, 58, 79, 13, 46, 77, 22, 52, 78, 40, 37, 43, 38, 35, 41, 39, 36, 42, 64, 28, 67, 62, 10, 65, 63, 19, 66, 76, 34, 61, 70, 16, 49, 73, 25, 55, 12, 45, 74, 21, 51, 75, 29, 26, 32, 30, 27, 33, 56, 9, 59, 57, 18, 60, 69, 15, 48, 72, 24, 54, 20, 50, 68, 11, 8, 14, 44, 17, 47, 71, 23, 53]
colswap[7] = [11, 3, 7, 15, 10, 2, 6, 14, 8, 0, 4, 12, 9, 1, 5, 13, 17, 16, 63, 60, 62, 65, 64, 61, 59, 57, 55, 58, 54, 56, 46, 47, 45, 42, 43, 44, 50, 52, 48, 49, 53, 51, 32, 31, 30, 34, 35, 33, 19, 20, 21, 22, 23, 18, 29, 24, 28, 26, 27, 25]