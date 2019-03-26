// TODO: - Change header path

#include "../../build/sdl2/arm64/SDL2-2.0.8/src/video/uikit/SDL_uikitviewcontroller.h"
#include "../../build/sdl2/arm64/SDL2-2.0.8/src/video/uikit/SDL_uikitappdelegate.h"

#import <GoogleMobileAds/GoogleMobileAds.h>
#import <Foundation/Foundation.h>

@interface KivyAdmob : NSObject {
    SDL_uikitviewcontroller *rootController;
    SDLUIKitDelegate *rootDelegate;
    GADBannerView *admodBanner;
    GADInterstitial *interstitial;
    GADRewardBasedVideoAd *rewardVideo;
}

@end
