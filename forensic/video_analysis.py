import cv2
import numpy as np

from forensic.deepfake_model import predict_frame



def video_check(file):


    cap = cv2.VideoCapture(file)


    if not cap.isOpened():

        return {

            "error":
            "Video gagal dibuka"

        }



    # ==============================
    # VIDEO INFORMATION
    # ==============================

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    duration = 0


    if fps > 0:

        duration = (
            total_frames / fps
        )



    if total_frames <= 0:

        cap.release()

        return {

            "error":
            "Video tidak memiliki frame"

        }



    # ==============================
    # SAMPLE FRAME
    # ==============================

    sample_count = min(
        20,
        total_frames
    )


    positions = np.linspace(
        0,
        total_frames - 1,
        sample_count,
        dtype=int
    )



    # ==============================
    # FORENSIC DATA
    # ==============================

    pixel_values = []

    brightness_values = []

    blur_values = []

    edge_values = []

    difference_values = []



    # ==============================
    # AI DATA
    # ==============================

    fake_values = []

    real_values = []



    previous_gray = None

    analyzed = 0



    # ==============================
    # ANALYSIS FRAME
    # ==============================

    for position in positions:


        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            int(position)
        )


        ret, frame = cap.read()



        if not ret:

            continue



        analyzed += 1



        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )



        # ------------------------------
        # Pixel variance
        # ------------------------------

        pixel = np.var(gray)

        pixel_values.append(
            float(pixel)
        )



        # ------------------------------
        # Brightness
        # ------------------------------

        brightness = np.mean(gray)

        brightness_values.append(
            float(brightness)
        )



        # ------------------------------
        # Blur score
        # ------------------------------

        blur = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()


        blur_values.append(
            float(blur)
        )



        # ------------------------------
        # Edge density
        # ------------------------------

        edges = cv2.Canny(
            gray,
            100,
            200
        )


        edge = (
            np.count_nonzero(edges)
            /
            edges.size
        )


        edge_values.append(
            float(edge)
        )



        # ------------------------------
        # Frame difference
        # ------------------------------

        if previous_gray is not None:


            diff = cv2.absdiff(
                gray,
                previous_gray
            )


            diff_score = np.mean(
                diff
            )


            difference_values.append(
                float(diff_score)
            )



        previous_gray = gray



        # ==============================
        # CNN PREDICTION
        # ==============================

        result = predict_frame(
            frame
        )


        if result:


            fake_values.append(
                result["fake"]
            )


            real_values.append(
                result["real"]
            )



    cap.release()



    if analyzed == 0:

        return {

            "error":
            "Tidak ada frame dianalisis"

        }



    # ==============================
    # AVERAGE FORENSIC
    # ==============================

    avg_pixel = np.mean(
        pixel_values
    )


    avg_brightness = np.mean(
        brightness_values
    )


    avg_blur = np.mean(
        blur_values
    )


    avg_edge = np.mean(
        edge_values
    )


    avg_difference = 0


    if len(difference_values) > 0:

        avg_difference = np.mean(
            difference_values
        )



    # ==============================
    # FORENSIC ANOMALY SCORE
    # ==============================

    anomaly_score = 0



    # blur rendah

    if avg_blur < 40:

        anomaly_score += 20



    # detail rendah

    if avg_edge < 0.02:

        anomaly_score += 20



    # brightness abnormal

    if (
        avg_brightness < 30
        or
        avg_brightness > 225
    ):

        anomaly_score += 20



    # perubahan frame

    if avg_difference > 45:

        anomaly_score += 20



    # pixel abnormal

    if avg_pixel > 7000:

        anomaly_score += 20




    anomaly_score = min(
        anomaly_score,
        100
    )



    # ==============================
    # MACHINE LEARNING RESULT
    # ==============================


    if len(fake_values) > 0:


        fake_probability = float(
            np.mean(
                fake_values
            )
        )


        real_probability = float(
            np.mean(
                real_values
            )
        )



    else:


        fake_probability = 0

        real_probability = 0





    # ==============================
    # FINAL DECISION
    # ==============================

    difference = abs(
        fake_probability -
        real_probability
    )



    if (

        fake_probability >= 75

        and

        difference >= 25

        and

        anomaly_score >= 30

    ):


        prediction = "DEEPFAKE"

        confidence = fake_probability



    elif (

        real_probability >= 75

        and

        difference >= 25

    ):


        prediction = "REAL"

        confidence = real_probability



    else:


        prediction = (
            "PERLU PEMERIKSAAN LANJUT"
        )


        confidence = max(
            fake_probability,
            real_probability
        )



    # ==============================
    # RETURN
    # ==============================

    return {


        "media_type":
        "video",



        "total_frame":
        total_frames,



        "frame_dianalisis":
        analyzed,



        "fps":
        round(
            float(fps),
            2
        ),



        "durasi_detik":
        round(
            float(duration),
            2
        ),



        # AI

        "prediction":
        prediction,



        "real_probability":
        round(
            real_probability,
            2
        ),



        "fake_probability":
        round(
            fake_probability,
            2
        ),



        "confidence":
        round(
            confidence,
            2
        ),



        # FORENSIC

        "anomaly_score":
        anomaly_score,



        "pixel_variance":
        round(
            float(avg_pixel),
            2
        ),



        "brightness":
        round(
            float(avg_brightness),
            2
        ),



        "blur_score":
        round(
            float(avg_blur),
            2
        ),



        "edge_density":
        round(
            float(avg_edge*100),
            2
        ),



        "frame_difference":
        round(
            float(avg_difference),
            2
        )

    }