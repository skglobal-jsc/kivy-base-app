// This code based on KivMob project of @MichaelStott
// Github: https://github.com/MichaelStott/KivMob

package biz.sk_global.admod;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.widget.LinearLayout;

import com.google.ads.mediation.admob.AdMobAdapter;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdSize;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.InterstitialAd;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.reward.RewardItem;
import com.google.android.gms.ads.reward.RewardedVideoAd;
import com.google.android.gms.ads.reward.RewardedVideoAdListener;
import com.google.android.gms.ads.AdListener;

import java.util.ArrayList;
import java.util.Dictionary;
import java.util.List;

import org.kivy.android.PythonActivity;

public class AdmodSupport {

    Activity _activity;
    AdView _adView;
    InterstitialAd _interstitial;
    RewardedVideoAd _rewarded;
    List<String> _test_devices;
    LayoutParams adLayoutParams;
    LinearLayout layout;
    boolean _loaded = false;
    AdMobRewardedVideoAdListener _listener;

    public AdmodSupport(final String appID) {
        _activity = PythonActivity.mActivity;
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                MobileAds.initialize(_activity, appID);
                _adView = new AdView(_activity);
                _interstitial = new InterstitialAd(_activity);
                _rewarded = MobileAds.getRewardedVideoAdInstance(_activity);
                _test_devices = new ArrayList<String>();
            }
        });
    }

    public void addTestDevices(final String testID) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _test_devices.add(testID);
            }
        });
    }

    public void newBanner(final String unitID, final boolean top_pos) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _adView = new AdView(_activity);
                _adView.setAdUnitId(unitID);
                _adView.setAdSize(AdSize.SMART_BANNER);
                _adView.setVisibility(View.GONE);
                LayoutParams adLayoutParams = new LayoutParams(
                        LayoutParams.MATCH_PARENT,
                        LayoutParams.WRAP_CONTENT);
                _adView.setLayoutParams(adLayoutParams);
                layout = new LinearLayout(_activity);
                if (!top_pos) {
                    layout.setGravity(Gravity.BOTTOM);
                }
                layout.addView(_adView);
                LayoutParams layoutParams = new LayoutParams(
                        LayoutParams.MATCH_PARENT,
                        LayoutParams.MATCH_PARENT);
                layout.setLayoutParams(layoutParams);
                _activity.addContentView(layout, layoutParams);
            }
        });

    }

    public void requestBanner(final Dictionary<String, Object> options) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _adView.loadAd(getBuilder(options));
            }
        });
    }

    public void showBanner() {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _adView.setVisibility(View.VISIBLE);
            }
        });
    }

    public void hideBanner() {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _adView.setVisibility(View.GONE);
            }
        });
    }

    public void newInterstitial(final String unitID) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _interstitial.setAdUnitId(unitID);
                _interstitial.setAdListener(new AdListener() {
                    @Override
                    public void onAdLoaded() {
                        super.onAdLoaded();
                        Log.d("python", "Inter Ad loaded");
                        _interstitial.show();
                    }

                    @Override
                    public void onAdClicked() {
                        super.onAdClicked();
                        Log.d("python", "Inter Ad clicked");
                    }

                    @Override
                    public void onAdClosed() {
                        super.onAdClosed();
                        Log.d("python", "Inter Ad close");
                    }
                });
            }
        });
    }

    public void requestInterstitial(final Dictionary<String, Object> options) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _interstitial.loadAd(getBuilder(options));
            }
        });
    }

    public boolean isInterstitialLoaded() {
        _loaded = _interstitial.isLoaded();
        return _loaded;
    }

    // public void showInterstitial(final Dictionary<String, Object> options) {
    //     _activity.runOnUiThread(new Runnable() {
    //         @Override
    //         public void run() {
    //             Log.d("python", "Interstitial is loaded: " + isInterstitialLoaded());
    //             if (!isInterstitialLoaded()) {
    //                 requestInterstitial(options);
    //             }
    //             _interstitial.show();
    //         }
    //     });
    // }

    public void setRewardedAdListener() {
        _listener = new AdMobRewardedVideoAdListener();
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _rewarded.setRewardedVideoAdListener(_listener);
            }
        });
    }

    public void loadRewardedAd(final String unitID) {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _rewarded.loadAd(unitID, getBuilder(null));
            }
        });
    }

    // public void showRewardedAd(final String unitID) {
    //     _activity.runOnUiThread(new Runnable() {
    //         @Override
    //         public void run() {
    //             if (!_rewarded.isLoaded()) {
    //                 loadRewardedAd(unitID);
    //             }
    //             // _rewarded.show();
    //         }
    //     });
    // }

    public void destroy_banner() {
        _activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                _adView.destroy();
            }
        });
    }

    public void destroyInterstitial() {
//        _interstitial.destroy();
    }

    public void destroyRewardedVideoAd() {
//        _rewarded.destroy();
    }

    private AdRequest getBuilder(Dictionary<String, Object> options) {
        AdRequest.Builder builder = new AdRequest.Builder();
        if (options != null && options.size() > 0) {
            if (options.get("children") != null) {
                builder.tagForChildDirectedTreatment((boolean)options.get("children"));
            }
            if (options.get("family") != null) {
                Bundle extras = new Bundle();
                extras.putBoolean(
                        "is_designed_for_families",
                        (boolean) options.get("family"));
                builder.addNetworkExtrasBundle(AdMobAdapter.class, extras);
            }
        }
        for(String item : _test_devices) {
            builder.addTestDevice(item);
        }

        return builder.build();
    }

    class AdMobRewardedVideoAdListener implements RewardedVideoAdListener {

        public static final String TAG = "python";

        @Override
        public void onRewardedVideoAdLoaded() {
            Log.d(TAG, "onRewardedVideoAdLoaded");
            _rewarded.show();
        }

        @Override
        public void onRewardedVideoAdOpened() {
            Log.d(TAG, "onRewardedVideoAdOpened");
        }

        @Override
        public void onRewardedVideoStarted() {
            Log.d(TAG, "onRewardedVideoStarted");
        }

        @Override
        public void onRewardedVideoAdClosed() {
            Log.d(TAG, "onRewardedVideoAdClosed");
        }

        @Override
        public void onRewarded(RewardItem rewardItem) {
            Log.d(TAG, "onRewarded");
        }

        @Override
        public void onRewardedVideoAdLeftApplication() {
            Log.d(TAG, "onRewardedVideoAdLeftApplication");
        }

        @Override
        public void onRewardedVideoAdFailedToLoad(int i) {
            Log.d(TAG, "onRewardedVideoAdFailedToLoad");
        }

        @Override
        public void onRewardedVideoCompleted() {
            Log.d(TAG, "onRewardedVideoCompleted");
        }
    }
}
