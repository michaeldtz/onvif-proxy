import cv2
import imutils
import time

def rotate_rtsp_stream(rtsp_url, output_url):
    """
    Greift einen RTSP-Stream ab, dreht ihn um 90 Grad und bietet ihn als neuen RTSP-Stream an.

    Args:
        rtsp_url (str): URL des Eingangs-RTSP-Streams.
        output_url (str): URL für den Ausgabe-RTSP-Stream.
    """

    # Capture den Eingangs-Stream
    cap = cv2.VideoCapture(rtsp_url)

    # Lege die Eigenschaften des Ausgabe-Streams fest
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_url, fourcc, 20.0, (640, 480))  # Passe die Auflösung an

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Drehe das Bild um 90 Grad im Uhrzeigersinn
        rotated = imutils.rotate_bound(frame, 90)

        out.write(rotated)

        # Zeige das Bild an (optional)
        cv2.imshow('Rotated Stream', rotated)
        if cv2.waitKey(1) == ord('q'):
            break

    # Release Ressourcen
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    print(cv2.getBuildInformation())
    
    # Beispielaufruf
    rtsp_input = 'rtsp://your_camera_ip/stream'
    rtsp_output = 'rtsp://your_server_ip/rotated_stream'
    rotate_rtsp_stream(rtsp_input, rtsp_output)