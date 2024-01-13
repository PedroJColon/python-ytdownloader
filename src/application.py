import customtkinter
from src.downloader import Downloader

# TODO: Allow for right click event to create up pop window


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # System Settings

        # TODO: Allow window to be resizable AND have all items in the app change size depending on how much was changed
        self.geometry("1280x720")
        customtkinter.set_appearance_mode("dark")
        self.title("Simple Youtube Downloader")
        self.resizable(True, True)

        self.option_values = ["Download Video", "Download Audio(mp3)", "Download Audio(wav)"]

        self.insert_text = customtkinter.CTkLabel(self, text="Insert Youtube Link Down Below")
        self.insert_text.pack(padx=10, pady=10)

        url_text = customtkinter.StringVar()
        self.link = customtkinter.CTkEntry(self, width=350, height=40, textvariable=url_text)
        self.link.pack(padx=10, pady=10)

        # Dropdown menu for downloading Audio or Video
        self.options = customtkinter.StringVar(value="Download Video")
        self.option_menu = customtkinter.CTkOptionMenu(self, values=[self.option_values[0],
                                                                     self.option_values[1],
                                                                     self.option_values[2]],
                                                       command=self.download_options,
                                                       variable=self.options)

        self.option_menu.pack(padx=15, pady=15)

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        # self.button.pack(padx=20, pady=20)

        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=50, pady=0)

        # Display video thumbnail underneath progress bar
        #TODO: Show Thumbnail of youtube video
        #thumbnail = customtkinter.CTkImage()
        #image_label = customtkinter.CTkLabel(self, image=thumbnail, text="")

        self.protocol("WM_DELETE_WINDOW")

    def download_options(self, options):
        download = Downloader()
        if options == self.option_values[0]:
            download.download_video(self.link.get())
        elif options == self.option_values[1]:
            download.download_audio(self.link.get(), ".mp3")
        elif options == self.option_values[2]:
            download.download_audio(self.link.get(), ".wav")