import customtkinter
from src.downloader import Downloader
from src.downloader import Status
from PIL import Image
import urllib.request
from io import BytesIO

# TODO: Allow for right click event to create up pop window

WIDTH: int = 1280
HEIGHT: int = 720


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # System Settings
        self.geometry(str(WIDTH) + "x" + str(HEIGHT))
        customtkinter.set_appearance_mode("dark")
        self.title("Simple Youtube Downloader")
        self.resizable(True, True)
        self.error = "No Youtube Video Downloaded Yet..."

        self.option_values = ["Download Video", "Download Audio (mp3)", "Download Audio (wav)",
                              "Download Playlist (Video)"]

        self.insert_text = customtkinter.CTkLabel(self, text="Insert Youtube Link Down Below")
        self.insert_text.pack(padx=10, pady=10)

        # Gets url text from user, This will be used in order to get the youtube videos specified
        url_text = customtkinter.StringVar()
        self.link = customtkinter.CTkEntry(self, width=350, height=40, textvariable=url_text)
        self.link.pack(padx=10, pady=10)

        # Dropdown menu for downloading Audio or Video
        self.options = customtkinter.StringVar(value="Download Video")
        self.option_menu = customtkinter.CTkOptionMenu(self, values=[self.option_values[0],
                                                                     self.option_values[1],
                                                                     self.option_values[2],
                                                                     self.option_values[3]],
                                                       command=self.download_options,
                                                       variable=self.options)

        self.option_menu.pack(padx=15, pady=15)

        # This was made in order to tell the user if the video is Downloaded, No Url was provided, or unavailable
        self.error_text = customtkinter.CTkLabel(self, text=self.error)
        self.error_text.pack(padx=10, pady=5)

        # Display video thumbnail underneath error_text.
        # Because we have no set image, we leave this blank and only update it once the video is downloaded
        self.image_label = customtkinter.CTkLabel(self, text="")
        self.image_label.pack(padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW")

    def download_options(self, options):
        download = Downloader()
        download_status = Status.NONE
        if options == self.option_values[0]:
            download_status = download.download_video(self.link.get())
        elif options == self.option_values[1]:
            download_status = download.download_audio(self.link.get(), ".mp3")
        elif options == self.option_values[2]:
            download_status = download.download_audio(self.link.get(), ".wav")
        elif options == self.option_values[3]:
            download_status = download.download_playlist(self.link.get())

        self.update_text(download_status)
        self.show_thumbnail(download.video.thumbnail_url)

    def update_text(self, download_status):
        match download_status:
            case Status.SUCCESS:
                self.error = "Download Success!"
                self.error_text.configure(text=self.error, text_color="LightGreen")
            case Status.UNAVAILABLE:
                self.error = "Download Failed..."
                self.error_text.configure(text=self.error, text_color="LightRed")
            case Status.NO_URL:
                self.error = "No Url Provided..."
                self.error_text.configure(text=self.error, text_color="LightYellow")

    def show_thumbnail(self, url):
        get_url = urllib.request.urlopen(url)
        url_data = get_url.read()
        get_url.close()  # Once we are done reading, close the url request
        # In case of different width and height values, this will automatically downsize the image to fit as thumbnail
        thumbnail_size_width: int = int(WIDTH / 2)
        thumbnail_size_height: int = int(HEIGHT / 2)
        img = customtkinter.CTkImage(dark_image=Image.open(BytesIO(url_data)),
                                     size=(thumbnail_size_width, thumbnail_size_height))
        self.image_label.configure(image=img)
