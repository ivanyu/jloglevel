package me.ivanyu;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class App
{
    public static void main(final String[] args) throws InterruptedException {
        final Logger logger = LoggerFactory.getLogger(App.class);
        while (true) {
            logger.debug("Hello");
            Thread.sleep(1000L);
        }
    }
}
