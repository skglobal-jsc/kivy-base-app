//
//  main.m
//  visibleFrame
//
//  Created by IVC on 1/21/19.
//  Copyright © 2019 demo. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Cocoa/Cocoa.h>
#import "visibleFrame.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSSize size = myfunc();
        printf("%s", [[NSString stringWithFormat:@"%.0f %.0f",size.width,size.height] UTF8String]);
    }
    return 0;
}
