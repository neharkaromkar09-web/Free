import os
import whisper
import moviepy.editor as mp

input_path = "input_video.mp4"
output_path = "output_video.mp4"

if os.path.exists(input_path):
    print("Whisper model loading...")
    model = whisper.load_model("base")
    
    print("Transcribing...")
    result = model.transcribe(input_path)
    segments = result["segments"]
    
    video = mp.VideoFileClip(input_path)
    edited_clips = []
    is_zoomed = False
    
    for segment in segments:
        sub_clip = video.subclip(segment["start"], segment["end"])
        if is_zoomed:
            zoomed_clip = sub_clip.resize(height=video.h * 1.25)
            final_sub_clip = zoomed_clip.crop(
                x_center=zoomed_clip.w / 2,
                y_center=zoomed_clip.h / 2,
                width=video.w,
                height=video.h
            )
        else:
            final_sub_clip = sub_clip
            
        edited_clips.append(final_sub_clip)
        is_zoomed = not is_zoomed
        
    final_video = mp.concatenate_videoclips(edited_clips)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("Editing Finished!")
else:
    print("Error: input_video.mp4 nahi mila!")
