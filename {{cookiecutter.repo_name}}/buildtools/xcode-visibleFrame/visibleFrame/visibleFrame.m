//
//  visibleFrame.m
//  visibleFrame
//
//  Created by IVC on 1/21/19.
//  Copyright © 2019 demo. All rights reserved.
//

#import "visibleFrame.h"

NSSize myfunc(){
    NSRect vRect = [[NSScreen mainScreen] visibleFrame];
    return vRect.size;
}
