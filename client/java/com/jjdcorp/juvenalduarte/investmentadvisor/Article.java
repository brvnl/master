package com.jjdcorp.juvenalduarte.investmentadvisor;

/**
 * Created by juvenalduarte on 23/10/16.
 */

public class Article {
    public String id;
    public String url;
    public String title;
    public String text;
    public String timestamp;

    public Article (String anId, String aTimestamp, String aUrl, String aTitle) {
        id = anId;
        url = aUrl;
        title = aTitle;
        timestamp = aTimestamp;
    }

    public Article (String rawServerData) {
        String[] parts = rawServerData.split("\\|");
        id = parts[0];
        url = parts[1];
        title = parts[2];
        timestamp = parts[3];
    }

    public String getDownloadRequest() {
        return "@fetchFullText;" + id;
    }

    public boolean isDownloaded() {
        return (text != null )? true: false;
    }

    public void setFullText(String fullText) {
        text = fullText;
    }
}
