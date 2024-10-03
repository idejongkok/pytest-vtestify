import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

class VisualAssertion:
    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.report_dir = "report/image"
        self.diff_path = os.path.join(self.report_dir, "diff.png")

    def compare_images(self, image1_path, image2_path):
        # Baca gambar
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # Ubah gambar ke grayscale
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Hitung SSIM antara dua gambar dan gambar perbedaannya
        score, diff = ssim(gray_image1, gray_image2, full=True)
        return score, diff

    def save_diff_image_with_boxes(self, image1_path, image2_path):
        score, diff = self.compare_images(image1_path, image2_path)
        diff = (diff * 255).astype("uint8")

        # Thresholding gambar perbedaan
        _, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        # Deteksi kontur
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Baca gambar asli
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # Buat salinan dari gambar asli untuk ditandai
        marked_image = image1.copy()

        # Gambarkan kotak pada perbedaan
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(marked_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Tambahkan teks pada pojok kiri bawah dari setiap gambar
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_color = (0, 255, 0)  # Warna teks
        font_thickness = 1

        # Tambahkan label pada gambar expected (gambar 1)
        cv2.putText(image1, "Expected Image", (10, image1.shape[0] - 10),
                    font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        # Tambahkan label pada gambar actual (gambar 2)
        cv2.putText(image2, "Actual Image", (10, image2.shape[0] - 10),
                    font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        # Tambahkan label pada gambar marked (gambar hasil diff)
        cv2.putText(marked_image, "Diff Image", (10, marked_image.shape[0] - 10),
                    font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        # Tambahkan border pada setiap gambar (gunakan warna hitam untuk batas)
        border_color = (0, 0, 0)  # Warna hitam
        border_thickness = 5  # Tebal border

        image1_with_border = cv2.copyMakeBorder(image1, border_thickness, border_thickness, border_thickness, border_thickness,
                                                cv2.BORDER_CONSTANT, value=border_color)
        image2_with_border = cv2.copyMakeBorder(image2, border_thickness, border_thickness, border_thickness, border_thickness,
                                                cv2.BORDER_CONSTANT, value=border_color)
        marked_image_with_border = cv2.copyMakeBorder(marked_image, border_thickness, border_thickness, border_thickness, border_thickness,
                                                      cv2.BORDER_CONSTANT, value=border_color)

        # Gabungkan gambar asli dan perbedaan yang ditandai
        combined = cv2.hconcat([image1_with_border, image2_with_border, marked_image_with_border])

        # Buat folder "report/image" jika belum ada
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

        # Simpan gambar perbedaan ke folder "report/image"
        cv2.imwrite(self.diff_path, combined)

        return score

    def assert_images(self, image1_path, image2_path):
        score = self.save_diff_image_with_boxes(image1_path, image2_path)
        print(f"SSIM between {image1_path} and {image2_path}: {score:.4f}")
        print(f"Diff image saved at: {self.diff_path}")
        assert score >= self.threshold, \
            f"Images {image1_path} and {image2_path} are not similar enough (SSIM: {score:.4f}, threshold: {self.threshold})."
