from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar, QSizePolicy)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice, QLegend
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtCore import Qt, QMargins
import logging

class GraphManager:
    def __init__(self):
        self.current_chart_widget = None
        # เก็บเป็น tuple ตั้งแต่ต้น เพื่อให้การเปรียบเทียบทำงานถูกต้อง
        self.last_values = (-1, -1, -1, -1)
        self.progress_bars = {}

    # ในไฟล์ graph_manager.py

    def update_chart_data(self, chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet):
        """อัปเดตข้อมูลในกราฟที่มีอยู่"""
        # ... (โค้ดเช็ค values_changed เดิมคงไว้) ...
        
        # ถ้าไม่มีการเปลี่ยนแปลง ให้ข้ามการอัปเดตเพื่อประหยัดงานวาด
        if not values_changed:
            logging.debug("update_chart_data skipped - values unchanged")
            return

        self.last_values = new_values
        try:
            # --- ส่วนที่ต้องเพิ่ม: คำนวณ Yield ใหม่ ---
            total_pcs = good_pcs + ng_pcs
            yield_val = (good_pcs / total_pcs * 100) if total_pcs > 0 else 0.0
            # -------------------------------------

            # ส่ง yield_val ไปยังฟังก์ชันอัปเดต (ต้องแก้การเรียกใช้ตามข้อ 1)
            self._update_summary_labels(chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet, yield_val)
            
            self._update_progress_bars(chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet)
            self._update_chart_series(chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet)
            
        except Exception as e:
            logging.exception("GraphManager.update_chart_data failed: %s", e)
    def _update_chart_series(self, chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet):
        """อัปเดตข้อมูลใน series ของกราฟ"""
        try:
            if not hasattr(chart_widget, 'chart_view'):
                return
                
            chart = chart_widget.chart_view.chart()
            if not chart:
                return
                
            # ค้นหา series ที่มีอยู่
            series_pcs = None
            series_sheet = None
            
            for series in chart.series():
                if series.name() == "PCS_Series":
                    series_pcs = series
                elif series.name() == "Sheet_Series":
                    series_sheet = series
                    
            # อัพเดต PCS series (วงใน)
            if series_pcs:
                series_pcs.clear()
                total_pcs = good_pcs + ng_pcs
                if total_pcs > 0:
                    good_slice = series_pcs.append(f"Good\n{good_pcs:,}", good_pcs)
                    good_slice.setColor(QColor("#4CAF50"))
                    ng_slice = series_pcs.append(f"NG\n{ng_pcs:,}", ng_pcs)
                    ng_slice.setColor(QColor("#F44336"))
                else:
                    no_data_slice = series_pcs.append("No Data", 1)
                    no_data_slice.setColor(QColor("#CCCCCC"))

            # อัพเดต Sheet series (วงนอก)
            if series_sheet:
                series_sheet.clear()
                total_sheet = good_sheet + ng_sheet
                if total_sheet > 0:
                    good_sheet_slice = series_sheet.append(f"Good Sheet\n{good_sheet:,}", good_sheet)
                    good_sheet_slice.setColor(QColor("#2196F3"))
                    ng_sheet_slice = series_sheet.append(f"NG Sheet\n{ng_sheet:,}", ng_sheet)
                    ng_sheet_slice.setColor(QColor("#E91E63"))
                else:
                    no_data_slice = series_sheet.append("No Data", 1)
                    no_data_slice.setColor(QColor("#999999"))
                    
        except Exception as e:
            logging.exception("_update_chart_series failed: %s", e)

    # ในไฟล์ graph_manager.py

    def _update_summary_labels(self, chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet, yield_percent=None):
        """อัปเดตค่าสรุปทั้งหมด รวมถึง Yield"""
        try:
            if not chart_widget:
                return
            
            # เตรียมข้อมูลสำหรับอัปเดต
            summary_labels = {
                "good_pcs": f"{good_pcs:,}",    # ใส่ลูกน้ำคั่นหลักพัน
                "ng_pcs": f"{ng_pcs:,}",
                "good_sheet": f"{good_sheet:,}",
                "ng_sheet": f"{ng_sheet:,}"
            }

            # เพิ่ม Yield เข้าไปถ้ามีค่าส่งมา
            if yield_percent is not None:
                summary_labels["yield_label"] = f"{yield_percent:.2f}%"
            
            for label_name, value in summary_labels.items():
                try:
                    # ค้นหา label โดย objectName
                    label = self._find_child_by_object_name(chart_widget, label_name)
                    if label and hasattr(label, 'setText'):
                        label.setText(value)
                        # logging.debug(f"Updated {label_name}: {value}")
                except Exception as e:
                    logging.debug(f"Could not update {label_name}: {e}")
                    
        except Exception as e:
            logging.exception("_update_summary_labels failed: %s", e)

    def _find_child_by_object_name(self, parent, object_name):
        """ค้นหา child widget โดยใช้ objectName"""
        if not parent:
            return None
            
        # ค้นหาใน children ทั้งหมด
        for child in parent.findChildren(QLabel):
            if child.objectName() == object_name:
                return child
                
        return None

    def create_double_donut_chart(self, good_pcs, ng_pcs, good_sheet, ng_sheet):
        """สร้างกราฟวงแหวนคู่พร้อมข้อมูลสรุป"""
        try:
            # ลองอัปเดตกราฟที่มีอยู่ก่อน
            if self.current_chart_widget:
                try:
                    self.update_chart_data(self.current_chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet)
                    return self.current_chart_widget
                except:
                    pass

            # คำนวณค่า Yield
            total_pcs = good_pcs + ng_pcs
            good_pcs_percentage = (good_pcs / total_pcs * 100) if total_pcs > 0 else 0
            
            # สร้าง container widget
            container = QWidget()
            container.setStyleSheet("""
                background-color: white; 
                border-radius: 10px;
                padding: 10px;
            """)
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # ส่วนกราฟ (ด้านซ้าย)
            chart = QChart()
            chart.setBackgroundBrush(QBrush(Qt.white))
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setMargins(QMargins(0, 0, 0, 30))

            # สร้างและตั้งค่า Series
            series_pcs = QPieSeries()
            series_pcs.setName("PCS_Series")
            series_sheet = QPieSeries()
            series_sheet.setName("Sheet_Series")

            # เพิ่มข้อมูล PCS (วงใน)
            if total_pcs > 0:
                good_slice = series_pcs.append(f"Good\n{good_pcs:,}", good_pcs)
                good_slice.setColor(QColor("#4CAF50"))
                ng_slice = series_pcs.append(f"NG\n{ng_pcs:,}", ng_pcs)
                ng_slice.setColor(QColor("#F44336"))
            else:
                no_data_slice = series_pcs.append("No Data", 1)
                no_data_slice.setColor(QColor("#CCCCCC"))

            series_pcs.setHoleSize(0.4)
            series_pcs.setPieSize(0.6)
            series_pcs.setLabelsVisible(False)

            # เพิ่มข้อมูล Sheet (วงนอก)
            total_sheet = good_sheet + ng_sheet
            if total_sheet > 0:
                good_sheet_slice = series_sheet.append(f"Good Sheet\n{good_sheet:,}", good_sheet)
                good_sheet_slice.setColor(QColor("#2196F3"))
                ng_sheet_slice = series_sheet.append(f"NG Sheet\n{ng_sheet:,}", ng_sheet)
                ng_sheet_slice.setColor(QColor("#E91E63"))
            else:
                no_data_slice = series_sheet.append("No Data", 1)
                no_data_slice.setColor(QColor("#999999"))

            series_sheet.setHoleSize(0.6)
            series_sheet.setPieSize(0.9)
            series_sheet.setLabelsVisible(False)

            # เพิ่ม Series ลงในกราฟ
            chart.addSeries(series_pcs)
            chart.addSeries(series_sheet)
            
            # ปรับแต่ง Legend
            chart.legend().setVisible(False)
            chart.legend().setAlignment(Qt.AlignRight)
            chart.legend().setFont(QFont("Arial", 10))
            chart.legend().setMarkerShape(QLegend.MarkerShapeCircle)
            chart.setAnimationOptions(QChart.AllAnimations)
            chart.setAnimationDuration(200)

            # สร้าง ChartView
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing, True)
            chart_view.setRenderHint(QPainter.SmoothPixmapTransform, True)
            chart_view.setStyleSheet("background: transparent;")
            
            # แก้ไข: เก็บ reference ถึง chart_view ใน container
            container.chart_view = chart_view
            # ส่วน Yield และข้อมูลสรุป (ด้านขวา)
            yield_widget = QWidget()
            yield_widget.setStyleSheet("background: transparent;")
            yield_layout = QVBoxLayout(yield_widget)
            yield_layout.setContentsMargins(0, 0, 0, 0)
            yield_layout.setSpacing(10)

            # สร้างและตั้งค่า Yield Label
            yield_label = QLabel(f"Yield: {good_pcs_percentage:.1f}%")
            yield_label.setObjectName("yieldLabel")
            yield_label.setAlignment(Qt.AlignLeft)
            yield_label.setStyleSheet("""
                QLabel {
                    font-size: 26px;
                    font-weight: bold;
                    color: #333333;
                    padding: 5px 0;
                    margin: 0;
                }
            """)

            # สร้างข้อมูลสรุป
            summary_data = [
                ("#4CAF50", "Good PCS", f"{good_pcs:,}", "good_pcs"),
                ("#F44336", "NG PCS", f"{ng_pcs:,}", "ng_pcs"),
                ("#2196F3", "Good Sheets", f"{good_sheet:,}", "good_sheet"),
                ("#E91E63", "NG Sheets", f"{ng_sheet:,}", "ng_sheet")
            ]

            # สร้าง container สำหรับข้อมูลสรุป
            summary_container = QWidget()
            summary_layout = QVBoxLayout(summary_container)
            summary_layout.setSpacing(0)
            summary_layout.setContentsMargins(0, 0, 0, 0)

            # เก็บ reference ถึง labels ไว้ใน container
            container.summary_labels = {}

            for color, label, value, object_name in summary_data:
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_layout.setContentsMargins(0, 0, 0, 0)
                item_layout.setSpacing(0)
                
                color_box = QLabel()
                color_box.setFixedSize(20, 20)
                color_box.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
                
                label_widget = QLabel(label)
                label_widget.setStyleSheet("font-size: 12px; font-weight: bold; color: #333333; min-width: 60px;")
                
                value_widget = QLabel(value)
                value_widget.setObjectName(object_name)  # ตั้ง objectName สำหรับค้นหา
                value_widget.setStyleSheet("font-size: 12px; font-weight: bold; color: #333333; min-width: 60px;")
                
                # เก็บ reference
                container.summary_labels[object_name] = value_widget
                
                item_layout.addWidget(color_box)
                item_layout.addWidget(label_widget)
                item_layout.addWidget(value_widget)
                item_layout.addStretch()
                
                summary_layout.addWidget(item_widget)

            # จัด Layout ด้านขวา
            yield_layout.addStretch()
            yield_layout.addWidget(yield_label)
            yield_layout.addWidget(summary_container)
            yield_layout.addStretch()
            
            # เพิ่มกราฟและข้อมูลลงใน container
            layout.addWidget(chart_view, stretch=7)
            layout.addWidget(yield_widget, stretch=3)
            
            self.current_chart_widget = container
            return container
            
        except Exception as e:
            logging.exception("Error in create_double_donut_chart")
            return QWidget()

    def display_plc_values(self, labels, values, scroll_area_contents):
        """Display defect values with modern progress bars - optimized for performance"""
        try:
            if scroll_area_contents is None:
                logging.warning("Scroll area contents is None")
                return

            layout = scroll_area_contents.layout()
            if not layout:
                logging.error("Layout not found in scroll_area_contents")
                return
            
            # Sort data by value (descending), then alphabetically
            sorted_data = sorted(zip(values, labels), key=lambda x: (-x[0], x[1]))
            max_value = max(values) if values else 1
            
            # เก็บลำดับของ labels ใหม่
            current_labels = [label for _, label in sorted_data]
            
            # ✅ เพิ่มตัวแปรเพื่อตรวจสอบว่าต้องสร้างใหม่ไหม
            needs_rebuild = False
            
            # ตรวจสอบว่าจำนวน widget ตรงกับจำนวน labels หรือไม่
            if len(self.progress_bars) != len(labels):
                needs_rebuild = True
            else:
                # ตรวจสอบว่า labels เปลี่ยนหรือไม่
                existing_labels = set(self.progress_bars.keys())
                new_labels = set(labels)
                if existing_labels != new_labels:
                    needs_rebuild = True
            
            if needs_rebuild:
                # ✅ จำเป็นต้องสร้างใหม่ (กรณีแรกหรือ labels เปลี่ยน)
                logging.debug("Rebuilding progress bars")
                
                # ล้าง layout
                while layout.count():
                    item = layout.takeAt(0)
                    if item and item.widget():
                        widget = item.widget()
                        # ลบเฉพาะ widget ที่ไม่ใช่ใน labels ใหม่
                        widget_label = widget.property("label")
                        if widget_label not in labels:
                            widget.deleteLater()
                
                # ล้าง progress_bars dictionary
                labels_to_remove = [lbl for lbl in self.progress_bars.keys() if lbl not in labels]
                for lbl in labels_to_remove:
                    del self.progress_bars[lbl]
                
                # สร้าง widget ใหม่ตามลำดับ
                for rank, (value, label_text) in enumerate(sorted_data):
                    if label_text not in self.progress_bars:
                        widget, bar, val_lbl, subtitle_lbl = self.create_progress_widget(
                            label_text, value, max_value, rank
                        )
                        # เก็บ label ใน widget property
                        widget.setProperty("label", label_text)
                        self.progress_bars[label_text] = (bar, val_lbl, widget, subtitle_lbl)
                        layout.addWidget(widget)
            else:
                # ✅ อัพเดตค่าใน widget ที่มีอยู่ (กรณีปกติ)
                logging.debug("Updating existing progress bars")
                
                # อัพเดตค่าและเรียงลำดับใหม่ถ้าต้องการ
                current_order = []
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        label = widget.property("label")
                        if label:
                            current_order.append(label)
                
                # ถ้าลำดับเปลี่ยน ให้เรียงใหม่
                if current_order != current_labels:
                    # ลบ widget ออกจาก layout (แต่ไม่ลบจาก memory)
                    for i in reversed(range(layout.count())):
                        item = layout.takeAt(i)
                    
                    # เพิ่มกลับตามลำดับใหม่
                    for label in current_labels:
                        if label in self.progress_bars:
                            _, _, widget, _ = self.progress_bars[label]
                            layout.addWidget(widget)
                
                # อัพเดตค่าในแต่ละ widget
                for rank, (value, label_text) in enumerate(sorted_data):
                    if label_text in self.progress_bars:
                        bar, val_lbl, widget, subtitle_lbl = self.progress_bars[label_text]
                        self._update_progress_widget(bar, val_lbl, subtitle_lbl, value, max_value, rank)
            
            scroll_area_contents.adjustSize()
            
        except Exception as e:
            logging.exception("Error in display_plc_values")

    def create_progress_widget(self, label, value, max_value, rank):
        """Create modern progress bar widget matching reference design"""
        try:
            widget = QWidget()
            widget.setMinimumHeight(70)
            
            # Main Layout: Horizontal (Left Content | Right Value)
            main_layout = QHBoxLayout()
            main_layout.setContentsMargins(10, 8, 10, 8)  # ลด margins ให้เล็กลง
            main_layout.setSpacing(15)  # ลด spacing
            
            # Left Container (Title, Bar, Subtitle)
            left_container = QWidget()
            left_layout = QVBoxLayout(left_container)
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.setSpacing(3)  # ลด spacing
            
            # Title Label
            text_lbl = QLabel(label)
            text_lbl.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background: transparent;
            """)
            
            # Progress Bar - ปรับให้กว้างขึ้น
            bar = QProgressBar()
            bar.setMaximum(max_value if max_value > 0 else 1)
            bar.setValue(value)
            bar.setFixedHeight(10)  # เพิ่มความสูงเล็กน้อย
            bar.setTextVisible(False)
            
            # ✅ ปรับ SizePolicy ให้ขยายเต็มที่มากขึ้น
            bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            # ✅ ตั้งค่า minimum width ให้ progress bar
            bar.setMinimumWidth(200)  # หรือค่าที่ต้องการ
            
            bar.setStyleSheet(self._get_modern_progress_style(value, rank))
            
            # Subtitle (Percentage or Count description)
            percent = (value / max_value * 100) if max_value > 0 else 0
            subtitle_lbl = QLabel(f"{value} pcs ({percent:.1f}%)")
            subtitle_lbl.setObjectName("subtitle")
            subtitle_lbl.setStyleSheet("""
                font-size: 11px;
                color: #7f8c8d;
                background: transparent;
            """)
            
            left_layout.addWidget(text_lbl)
            left_layout.addWidget(bar)
            left_layout.addWidget(subtitle_lbl)
            
            # ✅ ตั้ง stretch ให้ left_container ขยายมากกว่าเดิม
            left_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            # Right Container (Big Value / Icon)
            right_container = QWidget()
            right_layout = QVBoxLayout(right_container)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            val_lbl = QLabel(f"{value}")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            val_lbl.setStyleSheet("""
                font-size: 20px;
                font-weight: bold;
                color: #e74c3c; /* Red for defects */
                background: transparent;
            """)
            
            # ✅ ตั้ง fixed width ให้ right container เพื่อไม่ให้กินพื้นที่มากเกินไป
            right_container.setFixedWidth(60)
            
            right_layout.addWidget(val_lbl)
            
            # Add to main layout
            # ✅ ปรับ stretch ratio เป็น 10:1 (เดิมอาจจะเป็น 7:1 หรือ 5:1)
            main_layout.addWidget(left_container, stretch=12)  # เพิ่ม stretch
            main_layout.addWidget(right_container, stretch=1)
            
            widget.setLayout(main_layout)
            
            return widget, bar, val_lbl, subtitle_lbl
            
        except Exception as e:
            logging.exception("Error in create_progress_widget")
            return QWidget(), None, None, None

    def _get_modern_progress_style(self, value, rank):
        """Generate sleek gradient style for progress bar"""
        # Determine color based on rank/severity
        # Rank 0 (Highest) -> Red
        # Rank > 0 -> Orange/Yellow
        
        # Gradient definitions
        if rank == 0:
            # Red/Pink Gradient
            stops = "stop:0 #FF512F, stop:1 #DD2476"
        elif rank == 1:
            # Orange Gradient
            stops = "stop:0 #FF9966, stop:1 #FF5E62"
        elif rank == 2:
             # Yellow/Orange
            stops = "stop:0 #F09819, stop:1 #EDDE5D"
        else:
            # Blue/Green (Low priority) or Grey
            stops = "stop:0 #11998e, stop:1 #38ef7d"

        return f"""
            QProgressBar {{
                border: none;
                background-color: #ecf0f1; /* Light grey background */
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, {stops});
                border-radius: 4px;
            }}
        """

    def _update_progress_widget(self, bar, val_lbl, subtitle_lbl, value, max_value, rank):
        """Update widget values and style"""
        try:
            from PySide6.QtCore import QPropertyAnimation, QEasingCurve
            
            # Update max
            bar.setMaximum(max_value if max_value > 0 else 1)
            
            # Animate value
            if hasattr(bar, '_animation') and bar._animation:
                bar._animation.stop()
            
            animation = QPropertyAnimation(bar, b"value")
            animation.setDuration(400)
            animation.setStartValue(bar.value())
            animation.setEndValue(value)
            animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            animation.start()
            bar._animation = animation
            
            # Update labels
            val_lbl.setText(f"{value}")
            
            percent = (value / max_value * 100) if max_value > 0 else 0
            subtitle_lbl.setText(f"{value} pcs ({percent:.1f}%)")
            
            # Update colors if rank changed
            bar.setStyleSheet(self._get_modern_progress_style(value, rank))
            
            # Update text color based on density?
            # val_lbl.setStyleSheet(...) # Keep it red for now
            
        except Exception as e:
            logging.debug(f"Animation failed: {e}")
            bar.setValue(value)
            val_lbl.setText(f"{value}")
            percent = (value / max_value * 100) if max_value > 0 else 0
            subtitle_lbl.setText(f"{value} pcs ({percent:.1f}%)")
            bar.setStyleSheet(self._get_modern_progress_style(value, rank))

    def _update_progress_bars(self, chart_widget, good_pcs, ng_pcs, good_sheet, ng_sheet):
        try:
            # ตัวอย่างการอัพเดต progress bars หากมี
            if not chart_widget:
                return
            for name, widget in self.progress_bars.items():
                try:
                    # expected widget to be QProgressBar-like
                    widget.setValue(int(widget.value() if hasattr(widget, "value") else 0))
                except Exception:
                    pass
        except Exception as e:
            logging.exception("_update_progress_bars failed: %s", e)

    def cleanup(self):
        """Cleanup any resources held by GraphManager"""
        try:
            # ล้าง references เพื่อช่วย GC
            self.current_chart_widget = None
            # ถ้ามี progress bar widgets ที่ต้องลบ parent ให้ทำที่ caller
            self.progress_bars.clear()
            logging.debug("GraphManager.cleanup completed")
        except Exception as e:
            logging.exception("GraphManager.cleanup failed: %s", e)