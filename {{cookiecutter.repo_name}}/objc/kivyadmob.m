

#include "kivyadmob.h"


@implementation KivyAdmob

- (void) createAds{
    SDL_uikitviewcontroller *rootController = (SDL_uikitviewcontroller*)[[
        (SDLUIKitDelegate*)[[UIApplication sharedApplication] delegate] window] rootViewController];
#if DEBUG
    [GADMobileAds configureWithApplicationID:@"ca-app-pub-3940256099942544~1458002511"];
    NSString * bannerID = @"ca-app-pub-3940256099942544/2934735716";
#else
    // TODO: - Change Production id
    [GADMobileAds configureWithApplicationID:@"ca-app-pub-3940256099942544~1458002511"];
    NSString * bannerID = @"ca-app-pub-3940256099942544/2934735716";
#endif
    GADBannerView * admod = [[GADBannerView alloc]
                             initWithAdSize:kGADAdSizeBanner];
    CGSize screenSize = [[[UIApplication sharedApplication] delegate] window].frame.size;
    float height = 50.0;
    admod.frame = CGRectMake((screenSize.width - 320) / 2, screenSize.height - height, 320, height);

    [rootController.view addSubview:admod];
    [rootController.view bringSubviewToFront:admod];

    admod.adUnitID = bannerID;
    admod.rootViewController = rootController;

    [admod loadRequest:[GADRequest request]];
}

@end
