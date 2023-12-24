import math
from math import acos

import pdf2image
from PIL import ImageEnhance, Image, ImageOps


def find_horizontal_line(
        page: Image,
        min_line_length: int,
        max_hole: int,
        y_start: int = 0,
        x_start: int = 0,
        y_finish: int = 0,
        x_finish: int = 0
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None:
    print('Finding horizontal line')
    if y_finish == 0:
        y_finish = page.height
    if x_finish == 0:
        x_finish = page.width
    if x_finish - x_start < min_line_length:
        print('Horizontal line not found')
        return
    for y in range(y_start, y_finish):
        for x in range(x_start, x_finish):
            if page.getpixel((x, y)) == 0:
                x_line_finish = x
                y_line_finish = y_min = y_max = y
                while True:
                    if x_line_finish + 1 < x_finish:
                        x_line_finish += 1
                        if page.getpixel((x_line_finish, y_line_finish)) == 0:
                            continue
                    bypassed = False
                    for a_x in range(1, max_hole + 2):
                        for a_y in range(max_hole + 2):
                            if (x_line_finish + a_x < x_finish and y_line_finish - a_y > y_start and
                                    page.getpixel((x_line_finish + a_x, y_line_finish - a_y)) == 0):
                                y_line_finish -= a_y
                                y_min = min(y_min, y_line_finish)
                                bypassed = True
                                break
                            if (x_line_finish + a_x < x_finish and y_line_finish + a_y < y_finish and
                                    page.getpixel((x_line_finish + a_x, y_line_finish + a_y)) == 0):
                                y_line_finish += a_y
                                y_max = max(y_max, y_line_finish)
                                bypassed = True
                                break
                        if bypassed:
                            x_line_finish += a_x
                            break
                    if bypassed:
                        continue
                    if x_line_finish - x_start < min_line_length:
                        break
                    x_line_finish -= 1
                    x_line_start = x_line_finish
                    y_line_start = y_line_finish
                    while True:
                        if x_line_start < x_start + 1:
                            break
                        x_line_start -= 1
                        if page.getpixel((x_line_start, y_line_start)) == 0:
                            continue
                        bypassed = False
                        for a_x in range(1, max_hole + 2):
                            for a_y in range(max_hole + 2):
                                if (x_line_start - a_x > x_start and y_line_start - a_y > y_start and
                                        page.getpixel((x_line_start - a_x, y_line_start - a_y)) == 0):
                                    y_line_start -= a_y
                                    y_min = min(y_min, y_line_start)
                                    bypassed = True
                                    break
                                if (x_line_start - a_x > x_start and y_line_start + a_y < y_finish and
                                        page.getpixel((x_line_start - a_x, y_line_start + a_y)) == 0):
                                    y_line_start += a_y
                                    y_max = max(y_max, y_line_start)
                                    bypassed = True
                                    break
                            if bypassed:
                                x_line_start -= a_x
                                break
                        if bypassed:
                            continue
                        x_line_start += 1
                        break
                    if x_line_finish - x_line_start > min_line_length:
                        print('Founded horizontal line:',
                              (x_line_start, y_line_start),
                              (x_line_finish, y_line_finish))
                        return (x_line_start, y_line_start), (x_line_finish, y_line_finish), (y_min, y_max)
                    break
    print('Horizontal line not found')


def find_vertical_line(
        page: Image,
        min_line_length: int,
        max_hole: int,
        x_start: int = 0,
        y_start: int = 0,
        y_finish: int = 0,
        x_finish: int = 0
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None:
    print('Finding vertical line')
    if x_finish == 0:
        x_finish = page.width
    if y_finish == 0:
        y_finish = page.height
    if y_finish - y_start < min_line_length:
        print('Vertical line not found')
        return
    for x in range(x_start, x_finish):
        for y in range(y_start, y_finish):
            if page.getpixel((x, y)) == 0:
                x_line_finish = x_min = x_max = x
                y_line_finish = y
                while True:
                    if y_line_finish + 1 < y_finish:
                        y_line_finish += 1
                        if page.getpixel((x_line_finish, y_line_finish)) == 0:
                            continue
                    bypassed = False
                    for a_y in range(1, max_hole + 2):
                        for a_x in range(max_hole + 2):
                            if (x_line_finish - a_x > x_start and y_line_finish + a_y < y_finish and
                                    page.getpixel((x_line_finish - a_x, y_line_finish + a_y)) == 0):
                                x_line_finish -= a_x
                                x_min = min(x_min, x_line_finish)
                                bypassed = True
                                break
                            if (x_line_finish + a_x < x_finish and y_line_finish + a_y < y_finish and
                                    page.getpixel((x_line_finish + a_x, y_line_finish + a_y)) == 0):
                                x_line_finish += a_x
                                x_max = max(x_max, x_line_finish)
                                bypassed = True
                                break
                        if bypassed:
                            y_line_finish += a_y
                            break
                    if bypassed:
                        continue
                    if y_line_finish - y_start < min_line_length:
                        break
                    y_line_finish -= 1
                    x_line_start = x_line_finish
                    y_line_start = y_line_finish
                    while True:
                        if y_line_start < y_start + 1:
                            break
                        y_line_start -= 1
                        if page.getpixel((x_line_start, y_line_start)) == 0:
                            continue
                        bypassed = False
                        for a_y in range(1, max_hole + 2):
                            for a_x in range(max_hole + 2):
                                if (x_line_start - a_x > x_start and y_line_start - a_y > y_start and
                                        page.getpixel((x_line_start - a_x, y_line_start - a_y)) == 0):
                                    x_line_start -= a_x
                                    x_min = min(x_min, x_line_start)
                                    bypassed = True
                                    break
                                if (x_line_start + a_x < x_finish and y_line_start - a_y > y_start and
                                        page.getpixel((x_line_start + a_x, y_line_start - a_y)) == 0):
                                    x_line_start += a_x
                                    x_max = max(x_max, x_line_start)
                                    bypassed = True
                                    break
                            if bypassed:
                                y_line_start -= a_y
                                break
                        if bypassed:
                            continue
                        y_line_start += 1
                        break
                    if y_line_finish - y_line_start > min_line_length:
                        print('Founded vertical line:',
                              (x_line_start, y_line_start),
                              (x_line_finish, y_line_finish))
                        return (x_line_start, y_line_start), (x_line_finish, y_line_finish), (x_min, x_max)
                    break
    print('Vertical line not found')


def align_page(page: Image) -> Image:
    print('Aligning page')
    vertical_line = find_vertical_line(
        page,
        int(page.height * 0.75),
        3,
        0,
        0,
        0,
        int(page.width * 0.2))
    if vertical_line:
        if vertical_line[0][0] == vertical_line[1][0]:
            return page
        x_a = vertical_line[0][0]
        y_a = vertical_line[0][1]
        x_b = vertical_line[1][0]
        y_b = vertical_line[1][1]
        ab = ((x_b - x_a) ** 2 + (
                y_b - y_a) ** 2) ** 0.5
        ac = ((x_b - x_a) ** 2 + (
                y_a - y_a) ** 2) ** 0.5
        bc = ((x_b - x_b) ** 2 + (
                y_a - y_b) ** 2) ** 0.5
        angle = 90 - acos((ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab * ac)) * (180 / math.pi)
        if x_a < x_b:
            angle = -angle
        return page.rotate(angle, fillcolor=255)


def crop_table(page: Image) -> Image:
    print('Finding top and right sides of table')
    right = 0
    horizontal_line = find_horizontal_line(page, 200, 3)
    for i in range(2):
        if not horizontal_line:
            print('Data table not found')
            return
        cell_width = 0
        left = horizontal_line[0][0] + 5
        first_measure = True
        for right in range(left, int(page.width * 0.95)):
            cell_width = 0
            for y in range(horizontal_line[2][1] + 5, page.height):
                if cell_width > 99 or page.getpixel((right, y)) == 0:
                    break
                cell_width += 1
            if first_measure and (cell_width < 80 or cell_width > 99):
                break
            first_measure = False
            if cell_width > 99:
                noise_count = 0
                for a_x in range(5):
                    cell_width = 0
                    for y in range(horizontal_line[2][1] + 5, page.height):
                        if cell_width > 99 or page.getpixel((right + a_x, y)) == 0:
                            break
                        cell_width += 1
                    if cell_width < 100:
                        noise_count += 1
                if noise_count > 1:
                    continue
                break
        if not first_measure and cell_width > 99:
            break
        if i < 1:
            horizontal_line = find_horizontal_line(page, 200, 3, horizontal_line[2][1] + 10)
    else:
        print('Data table not found')
        return
    print('Finding left and bottom sides of table')
    left = horizontal_line[0][0] + 5
    top = horizontal_line[2][1] + 5
    cell_height = 0
    last_border_pixel = 0
    for x in range(left, int(page.width * 0.3)):
        if x > last_border_pixel:
            if page.getpixel((x, top)) == 0:
                if 24 < cell_height < 31:
                    left = x - cell_height
                    break
                for a_x in range(1, 5):
                    if page.getpixel((x + a_x, top)) == 0:
                        last_border_pixel = x + a_x
                cell_height = 0
                continue
            last_border_pixel = 0
            cell_height += 1
    else:
        print('Data table not found')
        return
    bottom = top
    for _ in range(10):
        horizontal_line = find_horizontal_line(page, int((right - left) * 0.5), 3, bottom + 30, left, 0, right)
        if not horizontal_line:
            print('Data table not found')
            return
        avg_start_finish_y = horizontal_line[0][1] + abs(horizontal_line[0][1] - horizontal_line[1][1]) // 2
        avg_min_max_y = horizontal_line[2][0] + (horizontal_line[2][1] - horizontal_line[2][0]) // 2
        bottom = min(avg_start_finish_y, avg_min_max_y) + abs(avg_start_finish_y - avg_min_max_y) // 2
    return page.crop((left, top, right, bottom))


def main():
    print('Opening PDF')
    start_page = 1
    pdf_pages = pdf2image.pdf2image.convert_from_path('test_res/test_pdfs/test.pdf',
                                                      first_page=start_page,
                                                      # last_page=start_page,
                                                      dpi=100,
                                                      poppler_path='poppler/Library/bin')
    for i, page in enumerate(pdf_pages):
        print(f'Page {start_page + i}, working')
        page = ImageEnhance.Contrast(page).enhance(10)
        for y in range(page.height):
            for x in range(page.width):
                pixel = page.getpixel((x, y))
                if max(pixel) - min(pixel) > 20:
                    page.putpixel((x, y), (255, 255, 255))
        page = page.point(lambda p: p > 180 and 255)
        page = page.convert('1')
        page = ImageOps.crop(page, 30)
        page = ImageOps.expand(page, 30, 255)
        page = align_page(page)
        if page:
            page = crop_table(page)
        if page:
            page.save(f'images/tabled/{start_page + i}.png')
            print(f'Page {start_page + i}, complete')


if __name__ == '__main__':
    main()
