import streamlit as st
import yt_dlp
import os
import glob

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Tahi Download Pro - Web Edition", page_icon="🚀")

st.title("🚀 TAHI DOWNLOAD PRO")
st.markdown("### Chuyên nghiệp - Tốc độ - Dễ nhìn (Web Version)")

# --- GIAO DIỆN NHẬP LIỆU ---
url = st.text_input("Dán link YouTube vào đây:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("Định dạng", ["Âm thanh (MP3)", "Video (MP4)"])
with col2:
    if mode == "Âm thanh (MP3)":
        quality = st.selectbox("Chất lượng", ["128kbps", "192kbps", "320kbps"], index=1)
    else:
        quality = st.selectbox("Độ phân giải", ["360p", "480p", "720p", "1080p"], index=2)

def download_video(link, mode, quality):
    # Cấu hình yt-dlp cho môi trường Web
    out_tmpl = "downloaded_file.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio/best' if mode == "Âm thanh (MP3)" else f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': 'temp_file', # Tên file tạm trên server
        'noplaylist': True,
        'quiet': True,
    }

    if mode == "Âm thanh (MP3)":
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality.replace("kbps", ""),
            }],
        })
    else:
        ydl_opts.update({'merge_output_format': 'mp4'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            # Tìm file vừa tải xong (yt-dlp có thể đổi đuôi file)
            files = glob.glob("temp_file*")
            if files:
                return files[0], info.get('title', 'video')
    except Exception as e:
        st.error(f"Lỗi: {e}")
        return None, None

# --- NÚT TẢI XUỐNG ---
if st.button("BẮT ĐẦU XỬ LÝ", use_container_width=True):
    if url:
        with st.spinner('Đang lấy dữ liệu từ YouTube... (Vui lòng chờ)'):
            file_path, title = download_video(url, mode, quality)
            
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.success(f"Đã xử lý xong: {title}")
                    st.download_button(
                        label="📥 BẤM VÀO ĐÂY ĐỂ LƯU VỀ MÁY",
                        data=f,
                        file_name=f"{title}.mp3" if mode == "Âm thanh (MP3)" else f"{title}.mp4",
                        mime="audio/mpeg" if mode == "Âm thanh (MP3)" else "video/mp4"
                    )
                # Xóa file tạm trên server sau khi chuẩn bị xong link tải
                os.remove(file_path)
    else:
        st.warning("Vui lòng nhập link!")