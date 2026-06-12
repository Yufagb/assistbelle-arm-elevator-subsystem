#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

int main(int argc, char *argv[]) {
    g_setenv("GST_DEBUG", "*:3,v4l2src:5,rtspserver:5,omxh264enc:5", TRUE);
    gst_init(&argc, &argv);

    // Create the main loop
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);

    // Create the RTSP server
    GstRTSPServer *server = gst_rtsp_server_new();
    gst_rtsp_server_set_service(server, "8554"); // Default RTSP port

    // Create the mount points
    GstRTSPMountPoints *mounts = gst_rtsp_server_get_mount_points(server);

    // Define the media factory with our pipeline
    GstRTSPMediaFactory *factory = gst_rtsp_media_factory_new();
    
    // MJPG from Logitech BRIO, decode, convert, encode to H264, RTP payload

    

    gst_rtsp_media_factory_set_launch(factory,
        "( v4l2src device=/dev/video0 ! image/jpeg, width=1920, height=1080, framerate=30/1 "
        "! jpegdec ! videoconvert ! x264enc tune=zerolatency bitrate=5000 speed-preset=ultrafast "
        "! rtph264pay name=pay0 pt=96 )"
    );

    gst_rtsp_media_factory_set_shared(factory, TRUE);

    // Attach the factory to /stream
    gst_rtsp_mount_points_add_factory(mounts, "/stream", factory);

    g_object_unref(mounts);

    // Attach the server to the default main context
    gst_rtsp_server_attach(server, NULL);

    g_print("RTSP server is live at rtsp://127.0.0.1:8554/stream\n");

    // Run the main loop
    g_main_loop_run(loop);

    return 0;
}
