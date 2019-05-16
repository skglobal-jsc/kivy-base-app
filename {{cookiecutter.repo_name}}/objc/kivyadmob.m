// To use this:
// - Download and extract file: http://dl.google.com/googleadmobadssdk/googlemobileadssdkios.zip
// - Open XCode and right-click to `Framework` folder, click `Add Files to "..." ...`
// - Click `Copy items if needed` and add all framework files just downloaded.
// - Add all files in `<project folder>/objc` to `Classes` folder with the same steps as above.
// - Open file `Resources/wordsfinder-Info.plist`, add:

// ```
// <key>GADApplicationIdentifier</key>
// <string>ca-app-pub-3940256099942544~1458002511</string>
// ```

// - To show banner this code:

// ```python
// from pyobjus import autoclass
// native_ads = autoclass('KivyAdmob').alloc().init_("ca-app-pub-3940256099942544~1458002511")
// native_ads.addAdmodBanner_("ca-app-pub-3940256099942544/2934735716")
// ```


#include "kivyadmob.h"


@implementation KivyAdmob

- (id) init: (NSString *) appID {
    if(self = [super init]) {
        rootController = (SDL_uikitviewcontroller*)[[(SDLUIKitDelegate*)[[UIApplication sharedApplication] delegate] window] rootViewController];
        rootDelegate = [[UIApplication sharedApplication] delegate];
#if DEBUG
        [GADMobileAds configureWithApplicationID:@"ca-app-pub-3940256099942544~1458002511"];
#else
        [GADMobileAds configureWithApplicationID: appID];
#endif
    }
    return self;
}

- (void) addAdmodBanner: (NSString *)idAd {
    if (admodBanner) {
        return;
    }
#if DEBUG
    NSString * bannerID = @"ca-app-pub-3940256099942544/2934735716";
#else
    NSString * bannerID = idAd;
#endif
    admodBanner = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner];
    CGSize screenSize = [rootDelegate window].frame.size;
    float height = 50.0;
    admodBanner.frame = CGRectMake((screenSize.width - 320) / 2, screenSize.height - height, 320, height);
    
    [rootController.view addSubview:admodBanner];
    [rootController.view bringSubviewToFront:admodBanner];
    
    admodBanner.adUnitID = bannerID;
    admodBanner.rootViewController = rootController;
    
    [admodBanner loadRequest:[GADRequest request]];
}

- (void) removeBanner {
    [admodBanner removeFromSuperview];
    admodBanner = NULL;
}

- (void) requestInterstitial: (NSString *)idAd {
    if (interstitial && !interstitial.hasBeenUsed) {
        return;
    }
#if DEBUG
    interstitial = [[GADInterstitial alloc]
                    initWithAdUnitID:@"ca-app-pub-3940256099942544/4411468910"];
#else
    interstitial = [[GADInterstitial alloc]
                    initWithAdUnitID:idAd];
#endif
    [interstitial loadRequest:[GADRequest request]];
}

- (Boolean) showInterstitial{
    if (interstitial.isReady) {
        [interstitial presentFromRootViewController:rootController];
        return true;
    }
    return false;
}

- (void) requestRewardVideoAd: (NSString *)idAd {
    if (rewardVideo && rewardVideo.isReady) {
        return;
    }
    rewardVideo = [GADRewardBasedVideoAd sharedInstance];
#if DEBUG
    [rewardVideo loadRequest:[GADRequest request]
                withAdUnitID:@"ca-app-pub-3940256099942544/1712485313"];
#else
    [rewardVideo loadRequest:[GADRequest request]
                withAdUnitID: idAd];
#endif
}

- (Boolean) showRewardVideoAd{
    if (rewardVideo.isReady) {
        [rewardVideo presentFromRootViewController:rootController];
        return true;
    }
    return false;
}

@end
