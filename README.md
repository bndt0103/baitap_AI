# AI Robot Vacuum Simulator (Mô phỏng Robot Hút Bụi AI)



- Dự án mô phỏng Agent Robot Hút Bụi (Vacuum Cleaner Agent) nhằm trực quan hóa và đánh giá hiệu năng của các thuật toán tìm kiếm (Search Algorithms) 
trong lĩnh vực Trí tuệ nhân tạo (AI). 

- Dự án được thiết kế chuẩn theo mô hình MVC và OOP hỗ trợ xuất log chi tiết để đối chiếu trực tiếp
với quá trình trace tay trên giấy.

## Mục lục
1. Mục đích 
2. Đầu vào & đầu ra (Input/ Output)
3. Các thuật toán hỗ trợ
4. Tính năng nổi bật
5. Kiến trúc thư mục
6. Hướng dẫn cài đặt
7. Hướng dẫn sử dụng

---------------------------------------------------

## 1. Mục đích dự án
- Mục đích: Giúp hiểu rõ cơ chế hoạt động của các cây tìm kiếm (Search Tree) thông qua việc trực quan hóa các tập Frontier (LIFO/FIFO/Priority Queue)
  và Reached/Explored.
- Thực tiễn: Cung cấp một môi trường (Environment) tùy biến để đánh giá, so sánh hiệu năng (thời gian, bộ nhớ, số node sinh ra)
  giữa các thuật toán Tìm kiếm mù (Uninformed) và Tìm kiếm có thông tin (Informed/Heuristic).

## 2. Đầu vào & Đầu ra (Input/Output)
- Đầu vào (Input)
    + Kích thước môi trường: Ma trận lưới (Grid) kích thước tùy chỉnh từ 1x1 đến 6x6
    + Trạng thái môi trường: Vị trí ngẫu nhiên của Robot, các chướng ngại vật (Obstacles) và các ô chứa rác (Dirts).
    + Cấu hình thuật toán: Lựa chọn thuật toán tìm kiếm và tốc độ mô phỏng (Animation Speed).
- Đầu ra (Output)
    + Log trace step: Quá trình duyệt cây chi tiết từng bước (Step-by-step) bao gồm trạng thái của:
      'Node', 'Action', 'Parent', 'Cost' và sự thay đổi của tập 'Frontier', 'Reached'.
    + Solution Path: Chuỗi hành động tối ưu hoặc thứ cấp để dọn sạch rác
      (Bao gồm các lệnh di chuyển 'UP', 'DOWN', 'LEFT', 'RIGHT' và lệnh hút rác 'Suck').
- Evaluation Metrics (Bảng đánh giá):
    + Tổng số bước (Total Steps).
    + Nodes Generated (Số node đã sinh ra).
    + Nodes Expanded (Số node đã duyệt/pop).
    + Max Frontier (Độ phức tạp không gian).
    + CPU Compute Time (Thời gian tính toán thực tế của thuật toán).

## 3. Các thuật toán hỗ trợ
Hệ thống hỗ trợ 9 biến thể của các thuật toán tìm kiếm:
- Tìm kiếm mù (Uninformed Search):
    + BFS Type 1: Breadth-First Search (Goal test sau khi POP - Queue FIFO).
    + BFS Type 2: Breadth-First Search (Goal test lúc sinh GENERATE).
    + DFS Type 1: Depth-First Search (Goal test sau khi POP - Stack LIFO).
    + DFS Type 2: Depth-First Search (Goal test lúc sinh GENERATE).
    + IDS Type 1 & 2: Iterative Deepening Search (Tìm kiếm sâu dần).
    + UCS: Uniform-Cost Search (Tìm kiếm chi phí đồng nhất).
- Tìm kiếm có thông tin (Informed / Heuristic Search):
    + Greedy Best-First Search: Sử dụng hàm Heuristic khoảng cách Manhattan.
    + A* Search: Tối ưu hóa với f(n) = g(n) + h(n) (Đảm bảo tìm đường ngắn nhất, xử lý khôi phục nhánh tối ưu).

## 4. Tính năng nổi bật
- Clean UI / UX: Giao diện chia 3 panel chuẩn Dashboard hiện đại, font chữ dễ nhìn, hỗ trợ Auto-scroll thông minh.
- Step-by-step Debugger: Cho phép chạy/dừng từng bước (Next Step / Pause / Resume) để phân tích lỗi thuật toán.
- Animation Smooth: Mô phỏng lại đường đi của Agent sau khi giải thuật hoàn tất với tốc độ realtime.
- Scalable Architecture: Dễ dàng thêm thuật toán mới chỉ bằng cách override class BaseSearch.

## 5. Kiến trúc thư mục
Dự án áp dụng mô hình thiết kế Modular chặt chẽ:
```text
vacuum_ai_projects/
│
├── algorithms/           # Chứa core logic của các thuật toán AI
│   ├── base_search.py    # Class cha (xử lý get_successors, đếm node)
│   ├── astar.py
│   ├── bfs_type1.py
│   └── ...
│
├── models/               # Định nghĩa cấu trúc dữ liệu
│   ├── node.py           # Class Node (Lưu state, parent, action, path_cost)
│   └── state.py          # Class State (Lưu vị trí robot và frozenset rác)
│
├── ui/                   # Chứa logic giao diện Tkinter
│   └── app.py            # Main GUI, Canvas, Layout & Render log
│
├── main.py               # Entry point (Điểm khởi chạy ứng dụng)
└── README.md
```
## 6. Hướng dẫn cài đặt
- Yêu cầu: python >= 3.8
- Khởi chạy:
    + Clone repository về máy:
      git clone https://github.com/your-username/vacuum_ai_projects.git
    + Di chuyển vào thư mục dự án
      cd vacuum_ai_projects
    + Chạy chương trình
      python main.py
## 7. Hướng dẫn sử dụng
- Khởi tạo môi trường: Tại Panel bên trái, chọn kích thước Rows x Cols mong muốn.
    + Nhấn Generate Map để tạo bản đồ ngẫu nhiên mới.
- Chọn thuật toán: Tick chọn một thuật toán trong danh sách Algorithms.
- Thực thi:
    + Nhấn Start / Reset để khởi tạo tiến trình.
    + Nhấn Next Step nếu muốn xem log chạy tay từng bước một.
    + Hoặc nhấn Auto Run để máy tự động dò đường. Có thể điều chỉnh thanh Log Auto Speed để tăng giảm tốc độ.
- Xem kết quả: Quan sát bảng ALGORITHM LOGS bên phải để xem cấu trúc Node.
    + Xem bảng FINAL SOLUTION PATH ở dưới cùng để lấy thống kê hiệu năng CPU.
## Tác giả:
- Họ và tên: Bùi Nguyễn Duy Trung
- MSSV: 24110363
- Môn học: Trí tuệ nhân tạo (AI)
