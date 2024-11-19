import cv2
import numpy as np
from scipy.spatial import distance
# 카메라에서 읽어온 프레임 좌우 반전


# 1. 실시간 카메라에서 가장자리 감지
def capture_and_detect_edges():
    """
    카메라로 이미지를 캡처하고 가장자리(엣지)를 감지하는 함수
    """

    cap = cv2.VideoCapture(0)  # 기본 카메라(0번) 열기
    
    if not cap.isOpened():
        raise Exception("Error: 카메라를 열 수 없습니다.")
    
    print("Press 'q' to capture the image and process edges...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: 프레임을 읽을 수 없습니다.")
            break
        frame = cv2.flip(frame, 1)  # 1은 좌우 반전을 의미
        # 흑백 변환 및 엣지 감지
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # 화면에 엣지 표시
        cv2.imshow("Live Edge Detection", edges)

        # 'q'를 눌러 이미지 캡처
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return edges  # 감지된 엣지 이미지 반환

# 2. 엣지 좌표 추출
def get_edge_coordinates(edges):
    """
    엣지 이미지에서 좌표를 추출하는 함수
    """
    coordinates = np.column_stack(np.where(edges > 0))  # 엣지의 좌표 추출
    return coordinates

# 3. 1cm 간격으로 샘플링
def sample_coordinates(coords, spacing_mm, pixel_to_mm_ratio):
    """
    좌표를 일정 간격으로 샘플링하는 함수
    """
    sampled_coords = [coords[0]]  # 첫 좌표 추가
    for i in range(1, len(coords)):
        dist = distance.euclidean(coords[i], sampled_coords[-1])
        if dist >= spacing_mm / pixel_to_mm_ratio:  # 간격 조건 충족 시 추가
            sampled_coords.append(coords[i])
    return np.array(sampled_coords)

# 4. 좌표 변환 (이미지 좌표 -> 로봇 좌표)
def convert_to_robot_coordinates(image_coords, pixel_to_mm_ratio, offset_x, offset_y):
    """
    이미지 좌표를 로봇 좌표로 변환하는 함수
    """
    robot_coords = []
    for coord in image_coords:
        x_robot = coord[1] * pixel_to_mm_ratio + offset_x  # X축 변환
        y_robot = coord[0] * pixel_to_mm_ratio + offset_y  # Y축 변환
        robot_coords.append((x_robot, y_robot))
    return robot_coords

# 5. 로봇 이동 명령 (모의 실행)
def move_robot_to(coord):
    """
    로봇 엔드 이펙터를 좌표로 이동시키는 함수 (여기서는 모의 실행)
    """
    print(f"로봇 이동: X={coord[0]:.2f}, Y={coord[1]:.2f}")

# 메인 실행 코드
if __name__ == "__main__":
    try:
        # 1. 카메라로부터 엣지 이미지 가져오기
        edges = capture_and_detect_edges()

        # 2. 엣지 좌표 추출
        edge_coords = get_edge_coordinates(edges)

        # 3. 좌표 샘플링 (1cm 간격)
        pixel_to_mm_ratio = 0.05  # 1픽셀당 0.05mm
        sampled_coords = sample_coordinates(edge_coords, spacing_mm=10, pixel_to_mm_ratio=pixel_to_mm_ratio)

        # 4. 로봇 좌표 변환 (이미지 좌표 -> 작업 좌표)
        offset_x, offset_y = 100, 200  # 로봇 기준 좌표계 오프셋(mm)
        robot_coords = convert_to_robot_coordinates(sampled_coords, pixel_to_mm_ratio, offset_x, offset_y)

        # 5. 로봇 이동
        print("로봇 경로 실행 시작:")
        for coord in robot_coords:
            move_robot_to(coord)

    except Exception as e:
        print(f"Error: {e}")
