import math
from math import acos

import pdf2image
from PIL import ImageEnhance, Image, ImageOps


def find_horizontal_line(
        page: Image,
        min_line_length: int,
        max_hole: int,
        y_start: int = 0, x_start: int = 0) -> tuple[tuple[int, int], tuple[int, int]]:
    print('Finding horizontal line')
    for y in range(y_start, page.height):
        for x in range(x_start, page.width):
            if page.getpixel((x, y)) == 0:
                x_line_finish = x
                y_line_finish = y
                line_length = 0
                while True:
                    if x_line_finish + 1 < page.width:
                        x_line_finish += 1
                        if page.getpixel((x_line_finish, y_line_finish)) == 0:
                            line_length += 1
                            continue
                        bypassed = False
                        for a_x in range(max_hole + 1):
                            for a_y in range(max_hole + 1):
                                if (x_line_finish + a_x < page.width and y_line_finish + a_y < page.height and
                                        page.getpixel((x_line_finish + a_x, y_line_finish + a_y)) == 0):
                                    y_line_finish += a_y
                                    bypassed = True
                                    break
                                if (x_line_finish + a_x < page.width and y_line_finish - a_y > 0 and
                                        page.getpixel((x_line_finish + a_x, y_line_finish - a_y)) == 0):
                                    y_line_finish -= a_y
                                    bypassed = True
                                    break
                            if bypassed:
                                x_line_finish += a_x
                                line_length += a_x
                                break
                        if bypassed:
                            continue
                        x_line_finish -= 1
                        x_line_start = x_line_finish
                        y_line_start = y_line_finish
                        line_length = 0
                        while True:
                            if x_line_start > 0:
                                x_line_start -= 1
                                if page.getpixel((x_line_start, y_line_start)) == 0:
                                    line_length += 1
                                    continue
                                bypassed = False
                                for a_x in range(max_hole + 1):
                                    for a_y in range(max_hole + 1):
                                        if (x_line_start - a_x > 0 and y_line_start + a_y < page.height and
                                                page.getpixel((x_line_start - a_x, y_line_start + a_y)) == 0):
                                            y_line_start += a_y
                                            bypassed = True
                                            break
                                        if (x_line_finish - a_x > 0 and y_line_start - a_y > 0 and
                                                page.getpixel((x_line_start - a_x, y_line_start - a_y)) == 0):
                                            y_line_start -= a_y
                                            bypassed = True
                                            break
                                    if bypassed:
                                        x_line_start -= a_x
                                        line_length += a_x
                                        break
                                if bypassed:
                                    continue
                                x_line_start += 1
                                if line_length > min_line_length:
                                    print('Founded horizontal line:',
                                          (x_line_start, y_line_start),
                                          (x_line_finish, y_line_finish))
                                    return (x_line_start, y_line_start), (x_line_finish, y_line_finish)
                            break
                        break


def align_page(page: Image) -> Image:
    print('Aligning page')
    horizontal_line = find_horizontal_line(page, 500, 3)
    x_a = horizontal_line[0][0]
    y_a = horizontal_line[0][1]
    x_b = horizontal_line[1][0]
    y_b = horizontal_line[1][1]
    ab = ((x_b - x_a) ** 2 + (
            y_b - y_a) ** 2) ** 0.5
    ac = ((x_b - x_a) ** 2 + (
            y_a - y_a) ** 2) ** 0.5
    bc = ((x_b - x_b) ** 2 + (
            y_a - y_b) ** 2) ** 0.5
    angle = acos((ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab * ac)) * (180 / math.pi)
    if y_a > y_b:
        angle = -angle
    return page.rotate(angle, fillcolor=255)


def main():
    poppler_path = 'poppler/Library/bin'
    print('Opening PDF')
    pdf_pages = pdf2image.pdf2image.convert_from_path('test_res/test_pdfs/test.pdf',
                                                      dpi=100,
                                                      poppler_path=poppler_path)
    for i, page in enumerate(pdf_pages):
        print(f'Page {i}, working')
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
        page.save(f'images/{i}.png')
        print(f'Page {i}, complete')


if __name__ == '__main__':
    main()
