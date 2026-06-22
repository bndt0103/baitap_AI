# Tổng hợp Dự án & Bài tập Trí Tuệ Nhân Tạo (AI)

Kho lưu trữ này tổng hợp các dự án và bài tập thực hành thuộc môn học Trí tuệ nhân tạo (AI). Nội dung bao phủ các chủ đề cốt lõi về tìm kiếm của AI, trải dài từ việc thiết kế các tác tử phản xạ (Reflex Agent) cơ bản, cho đến việc ứng dụng 6 nhóm thuật toán tìm kiếm đa dạng vào các môi trường mô phỏng thực tế như Robot hút bụi, bài toán tô màu bản đồ và game cờ Caro.

- **Demo tổng quan (Mô phỏng Vacuum Cleaner):**
<img width="1892" height="1008" alt="Thiết kế chưa có tên" src="https://github.com/user-attachments/assets/299e8e44-958f-4cba-a462-09c6c6bcb593" />

## Mục lục
1. Mục đích dự án
2. Tổng quan cấu trúc thư mục
3. Phân tích chi tiết 6 nhóm thuật toán AI
4. Tính năng nổi bật
5. Hướng dẫn cài đặt
6. Hướng dẫn sử dụng chung

---------------------------------------------------

## 1. Mục đích dự án
- **Về mặt học thuật**: Giúp nắm bắt vững vàng cơ chế hoạt động, sự khác biệt và ưu nhược điểm của từng thuật toán (Search Tree, CSP, Minimax...) thông qua việc trực quan hóa từng bước thực thi (step-by-step).
- **Về mặt thực tiễn**: Cung cấp một bộ các môi trường mô phỏng sinh động, cho phép tinh chỉnh cấu hình để đối chiếu và đánh giá hiệu năng thực tế (thời gian tính toán, độ phức tạp không gian, số lượng node sinh ra và mở rộng) của các hệ thống AI.

## 2. Tổng quan cấu trúc thư mục
Dự án được phân bổ mạch lạc theo từng chủ đề học tập. Các file và thư mục chính bao gồm:

- 📂 **`vacuum_ai_projects/`**: Dự án mô phỏng Robot Hút Bụi (Vacuum Cleaner Agent). Hệ thống này tích hợp giao diện hiện đại và bao gồm 4 nhóm thuật toán tìm kiếm trên không gian trạng thái (Uninformed, Informed, Local Search, Complex Environments).
- 📄 **`coloring_map_tiengiang.ipynb`**: File Jupyter Notebook giải quyết bài toán tô màu bản đồ hành chính tỉnh Tiền Giang (trên ảnh thực tế). Áp dụng nhóm thuật toán Thỏa mãn ràng buộc (CSP).
- 📄 **`caro_game.ipynb`**: File Jupyter Notebook chứa game Cờ Caro, ứng dụng nhóm thuật toán Tìm kiếm đối kháng (Adversarial Search) để xây dựng AI đối đầu trực tiếp với người chơi.
- 📂 **`model_based_reflex_agent/`**: Mô phỏng tác tử có trạng thái (Model-based Agent), tích hợp bộ nhớ lưu trữ lịch sử môi trường cho các bài toán sơ cấp.
- 📂 **`simple_reflex_sgent/`**: Mô phỏng tác tử phản xạ đơn giản (Simple Reflex Agent), hành động hoàn toàn dựa trên cảm nhận tức thời tại thời điểm hiện tại.
- 📂 **`BFS/`**: Thư mục chứa các bài tập nền tảng nhằm làm quen với thuật toán tìm kiếm theo chiều rộng (Breadth-First Search).

## 3. Phân tích chi tiết 6 nhóm thuật toán AI
Toàn bộ các thuật toán trong repository được cài đặt bám sát tư duy học thuật từ giáo trình tiêu chuẩn Russell. Chi tiết cụ thể như sau:

### 🌟 Nhóm 1 đến 4: (Tích hợp trong dự án Robot Hút Bụi - `vacuum_ai_projects/`)

**1. Tìm kiếm mù (Uninformed Search)**
Giải quyết bài toán bằng cách duyệt qua không gian trạng thái đơn thuần mà không có bất kỳ thông tin gợi ý nào về khoảng cách đến mục tiêu.
- **Breadth-First Search (BFS)**: Duyệt cây tìm kiếm theo từng mức (chiều rộng). Luôn đảm bảo tìm được đường đi ngắn nhất (về số bước di chuyển), nhưng tiêu tốn bộ nhớ lớn do phải lưu trữ toàn bộ các node cùng mức vào tập biên (Frontier).
- **Depth-First Search (DFS)**: Khám phá sâu nhất có thể dọc theo mỗi nhánh trước khi quay lui (backtracking). Tiết kiệm bộ nhớ hơn BFS, nhưng dễ bị kẹt ở các nhánh vô hạn và không đảm bảo tìm ra đường đi tối ưu.
- **Iterative Deepening Search (IDS)**: Kết hợp ưu điểm của BFS và DFS. Thuật toán tiến hành tìm kiếm sâu dần với giới hạn độ sâu tăng dần qua từng bước lặp, vừa tối ưu bộ nhớ (đặc tính của DFS) vừa đảm bảo tính hoàn thiện (đặc tính của BFS).
- **Uniform-Cost Search (UCS)**: Liên tục mở rộng node có chi phí đường đi g(n) thấp nhất. Đây là lựa chọn hoàn hảo khi các hành động có mức hao phí khác nhau, đảm bảo đường đi cuối cùng có tổng chi phí nhỏ nhất.

**2. Tìm kiếm có thông tin / Khám phá Heuristic (Informed Search)**
Sử dụng hàm đánh giá Heuristic h(n) để ước lượng chi phí từ trạng thái hiện tại đến đích, giúp thuật toán "định hướng" và ưu tiên duyệt các nhánh tiềm năng. Trong bài toán không gian lưới, hàm Heuristic thường được sử dụng là khoảng cách Manhattan.
- **Greedy Best-First Search**: Luôn ưu tiên mở rộng node có giá trị h(n) nhỏ nhất. Thuật toán này tìm đến đích rất nhanh nhưng thường bỏ lỡ các đường đi tối ưu thực sự.
- **A\* Search**: Khắc phục nhược điểm của Greedy bằng cách dùng hàm đánh giá f(n) = g(n) + h(n) (tổng chi phí thực tế + chi phí ước lượng). A* cân bằng tốt giữa tốc độ và tính chính xác, luôn đảm bảo tìm được đường đi tối ưu nhất (với điều kiện hàm Heuristic thỏa mãn tính chấp nhận được - Admissible).

**3. Tìm kiếm cục bộ (Local Search)**
Thay vì lưu trữ toàn bộ cây tìm kiếm (rất hao phí tài nguyên đối với các bài toán không gian lớn), hướng tiếp cận này chỉ duy trì trạng thái hiện tại và nỗ lực di chuyển sang các trạng thái lân cận có giá trị tốt hơn.
- **Hill Climbing**: Liên tục di chuyển về phía trạng thái lân cận tốt hơn (leo lên đỉnh đồi). Nhược điểm lớn nhất là dễ bị mắc kẹt tại các "cực đại cục bộ" (Local Maxima) mà không thể tiếp cận cực đại toàn cục.
- **Simulated Annealing (Luyện kim)**: Đưa yếu tố ngẫu nhiên vào để thoát khỏi cực đại cục bộ. Ở giai đoạn đầu, thuật toán sẵn sàng chấp nhận các trạng thái tồi hơn với xác suất cao, sau đó xác suất này giảm dần theo "nhiệt độ" (Temperature) giống hệt như quá trình làm nguội kim loại.
- **Local Beam Search**: Theo dõi đồng thời k trạng thái tốt nhất thay vì chỉ 1 trạng thái. Tại mỗi bước lặp, thuật toán tạo ra tất cả các trạng thái lân cận của k trạng thái này, đánh giá và chọn lọc ra đúng k trạng thái tốt nhất để tiếp tục.

**4. Khám phá trong môi trường phức tạp (Complex Environments / Nondeterministic)**
Xử lý bài toán trong môi trường không xác định, nơi một tác động có thể dẫn đến nhiều hệ quả ngẫu nhiên khác nhau.
- **And-Or Graph Search**: Xây dựng một kế hoạch điều kiện (Contingency plan) thay vì một chuỗi hành động tuyến tính. Khi gặp node OR (do tác tử quyết định), thuật toán lựa chọn một nhánh khả thi; khi gặp node AND (do môi trường phản hồi), thuật toán phải bao quát và dự phòng cho mọi tình huống có thể xảy ra.

### 🌟 Nhóm 5: Thỏa mãn ràng buộc - CSP (Tích hợp trong `coloring_map_tiengiang.ipynb`)
**5. Constraint Satisfaction Problems (CSP)**
Giải quyết bài toán tô màu bản đồ tỉnh Tiền Giang. Mục tiêu cốt lõi là gán màu cho các huyện sao cho không có bất kỳ 2 huyện liền kề nào (có chung biên giới) bị trùng màu, tuân thủ chặt chẽ ràng buộc đồ thị.
- **Backtracking (Quay lui)**: Khám phá không gian biến. Gán màu cho từng biến (huyện), nếu phát hiện vi phạm ràng buộc thì lập tức quay lui (backtrack) để thử một màu khác.
- **Forward Checking (Kiểm tra tới)**: Kỹ thuật dự báo sớm. Mỗi khi gán màu cho một huyện, thuật toán sẽ sàng lọc và loại bỏ màu đó khỏi miền giá trị của tất cả các huyện lân cận. Nếu có huyện lân cận cạn kiệt màu khả dĩ, nó lập tức quay lui để tiết kiệm đáng kể thời gian duyệt nhánh vô ích.
- **AC-3 (Arc Consistency 3)**: Kiểm tra và đảm bảo tính nhất quán trên các cung (arc) trước và trong quá trình gán. Nó liên tục thu hẹp không gian tìm kiếm bằng cách loại bỏ các giá trị không thỏa mãn khỏi miền khả dĩ của các biến.
- **Min-Conflicts**: Một biến thể của tìm kiếm cục bộ áp dụng cho CSP. Thuật toán khởi đầu bằng việc gán ngẫu nhiên màu cho toàn bộ bản đồ (chấp nhận có lỗi vi phạm), sau đó liên tục khoanh vùng các huyện đang vi phạm ràng buộc và đổi màu của chúng sang màu gây ra ít xung đột nhất với các vùng xung quanh.

> **Minh họa thuật toán CSP (Tô màu bản đồ):**
<img width="1918" height="1018" alt="coloring_map_tiengiang" src="https://github.com/user-attachments/assets/381c084a-49b2-4b23-a2ee-25b2fdaef41b" />


### 🌟 Nhóm 6: Tìm kiếm đối kháng (Tích hợp trong `caro_game.ipynb`)
**6. Adversarial Search**
Xây dựng AI đánh Cờ Caro. Khác biệt cốt lõi so với các bài toán một Agent là sự cạnh tranh khốc liệt giữa 2 người chơi (AI và con người), nơi hành động của đối thủ sẽ ảnh hưởng trực tiếp đến không gian trạng thái của mình.
- **Minimax**: Thuật toán duyệt cây trò chơi (Game tree). Nó giả định người chơi AI (đóng vai Max) luôn nỗ lực tối đa hóa điểm số, trong khi con người (đóng vai Min) luôn nỗ lực tối thiểu hóa điểm số của AI. Thuật toán sẽ tính toán ngược từ dưới lên để tìm ra nước đi an toàn nhất dựa trên giả định cả hai bên đều đánh tối ưu.
- **Alpha-Beta Pruning (Tỉa nhánh Alpha-Beta)**: Là bản nâng cấp hoàn hảo của Minimax. Bằng cách duy trì 2 ranh giới cận alpha và beta, thuật toán nhận diện và cắt tỉa (loại bỏ) những nhánh không có khả năng mang lại kết quả tốt hơn những gì đã khám phá. Điều này giúp cắt giảm hàng triệu phép tính toán vô ích mà vẫn bảo toàn 100% tính chính xác của Minimax.

> **Minh họa thuật toán Đối kháng (Game Caro):**
<img width="387" height="600" alt="caro_game" src="https://github.com/user-attachments/assets/b41cc676-e366-4e2b-9f13-a49cb7a82471" />


## 4. Tính năng nổi bật
- **Giao diện trực quan & Animation (Clean UI)**: Hệ thống sử dụng các thư viện UI (Tkinter, Pygame, OpenCV) mang đến không gian tương tác hiện đại. Animation chuyển động mượt mà giúp người xem dễ dàng bám sát quá trình xử lý của thuật toán.
- **Trace Step-by-step Debugger**: Khả năng dừng/chạy từng bước. Giao diện tự động in log và thống kê chi tiết chi phí, cấu trúc node, rất thích hợp để đối chiếu với quá trình dò thuật toán trên giấy.
- **Tương tác trực tiếp qua Notebook**: Tận dụng Jupyter Notebook cho các bài toán nâng cao (Cờ Caro, Tô màu) kết hợp Widget. Vừa cung cấp một môi trường giải thích code thân thiện, vừa hỗ trợ khả năng "Play" và thử nghiệm trực tiếp ngay trong khối lệnh.
- **Đa dạng môi trường AI**: Trải dài từ các mô phỏng một tác tử (Single Agent) xử lý bài toán tuyến tính, đến các bài toán đối kháng đa luồng tư duy phức tạp.

## 5. Hướng dẫn cài đặt
- **Yêu cầu môi trường**: `python >= 3.8`, môi trường `Jupyter Notebook`.
- **Khởi chạy**:
    1. Tiến hành Clone repository về thiết bị cục bộ:
       ```bash
       git clone https://github.com/your-username/Baitap_AI.git
       ```
    2. Truy cập vào thư mục của dự án:
       ```bash
       cd Baitap_AI
       ```
    3. (Tùy chọn) Cài đặt các thư viện phụ thuộc nếu có báo lỗi thiếu (ví dụ: `pygame`, `opencv-python`, `pillow`, `ipywidgets`):
       ```bash
       pip install pygame opencv-python pillow ipywidgets
       ```

## 6. Hướng dẫn sử dụng chung
- **Đối với Dự án `vacuum_ai_projects`**: 
  - Mở terminal tại thư mục này và khởi chạy lệnh `python main.py`. 
  - Tùy chỉnh tham số Map và chọn 1 trong 4 nhóm thuật toán tìm kiếm cơ bản để quan sát mô phỏng.
- **Đối với bài toán `coloring_map_tiengiang.ipynb`**: 
  - Khởi chạy file thông qua Jupyter Notebook, chọn **Run All**. Giao diện ứng dụng tải ảnh lên và mô phỏng quá trình kiểm tra ràng buộc CSP sẽ hiển thị.
- **Đối với `caro_game.ipynb`**: 
  - Khởi chạy file qua Jupyter Notebook, chọn **Run All**. Bàn cờ Caro tương tác sẽ xuất hiện để bạn đấu trí với AI.
- **Đối với các thư mục cơ bản (BFS, Reflex Agents)**:
  - Mở Terminal chạy file `python <tên_file>.py` để xem output hiển thị dưới dạng Text Log.

---------------------------------------------------
## Tác giả
- **Họ và tên**: Bùi Nguyễn Duy Trung
- **MSSV**: 24110363
- **Môn học**: Trí tuệ nhân tạo (AI)
