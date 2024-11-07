from onvif import OnvifClient


if __name__ == '__main__':
    #onvif_client = OnvifClient('192.168.1.109', 8000, 'SynCamUser', 't35x$q771')
    onvif_client = OnvifClient('192.168.1.244', 8200, 'SynCamUser', 't35x$q771')
    #onvif_client = OnvifClient('127.0.0.1', 8001, 'SynCamUser', 't35x$q771')
    profile_tokens = onvif_client.get_profile_tokens()

    #media2_service = onvif_client._onvif_camera.create_media2_service()
    #profile_tokens = [profile.Name for profile in media2_service.GetProfiles()]

    for profile_token in profile_tokens:
        print(f"token {profile_token}")
        streamingURL = onvif_client.get_streaming_uri(profile_token)
        print(f"streaming: {streamingURL}")

    
