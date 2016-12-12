package com.jjdcorp.juvenalduarte.investmentadvisor;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import android.os.AsyncTask;
import java.net.InetAddress;
import java.net.Socket;
import java.util.Iterator;
import java.util.List;
import java.util.LinkedList;
import java.util.concurrent.TimeUnit;
import android.widget.ProgressBar;

/**
 * Created by juvenalduarte on 23/10/16.
 */

public class ServerData{

    public interface DataServerListener {
        public void onDownloadingData();
        public void onStoreReady();
    }

    public int articleIndex;
    private static ServerData instance = null;
    public DataServerListener listener;
    public List<Article> articles;
    public String host;
    public int port;
    Socket soc;

    protected ServerData (){
        this.port = ServerDetails.getDataServerHostPort();
        this.host = ServerDetails.getDataServerHostIP();
        this.listener = null;
        this.articleIndex = -1;
    }

    public static ServerData getInstance() {
        if(instance == null) {
            instance = new ServerData();
        }
        return instance;
    }

    public static ServerData reset() {
        instance = new ServerData();
        return instance;
    }

    public void setCustomObjectListener(DataServerListener listener) {
        this.listener = listener;
    }

    public boolean fetchArticles(String user, String password, String feeders, int timewd){

        // Connecting to the server
        try{
            InetAddress serverAddr = InetAddress.getByName(this.host);
            this.soc = new Socket(serverAddr,this.port);
        }catch(Exception e){
            e.printStackTrace();
            this.soc = null;
            System.out.println("DEBUG* Failed to get a socket on Fetch Article");
            return false;
        }

        // Adding articles to the list. Receiving data from the server.
        this.articles = new LinkedList<Article>();
        System.out.println("DEBUG* Got a socket on Fetch Article");
        String request = "@fetchUserArticles;user:" + user + ";password:" + password + ";feeders:" + feeders + ";timewindow:" + timewd;
        try {
            DataOutputStream dout = new DataOutputStream(soc.getOutputStream());
            dout.writeUTF(request);

            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));
            String incoming = "";

            while ((incoming = br.readLine()) != null) {
                System.out.println("DEBUG* Incoming on Fetch Article: " + incoming);
                if (incoming.replace("\n", "").replace("\r", "").contentEquals("Done")) {
                    break;
                }
                Article newArticle = new Article(incoming);
                this.articles.add(newArticle);
            }

            dout.flush();
            dout.close();

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                this.soc.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // Downloading full content for each article
        Iterator<Article> it = articles.iterator();
        while (it.hasNext()) {
            Article current = it.next();
            downloadArticle(current);
        }

        this.articleIndex = 0;
        return true;
    }

    public boolean fetchArticles(String user, String password){

        // Connecting to the server
        try{
            InetAddress serverAddr = InetAddress.getByName(this.host);
            this.soc = new Socket(serverAddr,this.port);
        }catch(Exception e){
            e.printStackTrace();
            this.soc = null;
            System.out.println("DEBUG* Failed to get a socket on Fetch Article");
            return false;
        }

        // Adding articles to the list. Receiving data from the server.
        this.articles = new LinkedList<Article>();
        System.out.println("DEBUG* Got a socket on Fetch Article");
        String request = "@fetchUserArticles;user:" + user + ";password:" + password;
        try {
            DataOutputStream dout = new DataOutputStream(soc.getOutputStream());
            dout.writeUTF(request);

            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));
            String incoming = "";

            while ((incoming = br.readLine()) != null) {
                System.out.println("DEBUG* Incoming on Fetch Article: " + incoming);
                if (incoming.replace("\n", "").replace("\r", "").contentEquals("Done")) {
                    break;
                }
                Article newArticle = new Article(incoming);
                this.articles.add(newArticle);
            }

            dout.flush();
            dout.close();

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                this.soc.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // Downloading full content for each article
        Iterator<Article> it = articles.iterator();
        while (it.hasNext()) {
            Article current = it.next();
            downloadArticle(current);
        }

        this.articleIndex = 0;
        return true;
    }

    public boolean downloadArticle(Article anArticle){
        try{
            InetAddress serverAddr = InetAddress.getByName(this.host);
            this.soc = new Socket(serverAddr,this.port);
        }catch(Exception e){
            e.printStackTrace();
            this.soc = null;
            return false;
        }

        String request = anArticle.getDownloadRequest();
        StringBuilder fullText = new StringBuilder();
        try {
            DataOutputStream dout = new DataOutputStream(soc.getOutputStream());
            dout.writeUTF(request);

            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));
            String incoming = "";

            while ((incoming = br.readLine()) != null) {
                if (incoming.replace("\n", "").replace("\r", "").contentEquals("Done")) {
                    break;
                }
                fullText.append(incoming);
            }

            dout.flush();
            dout.close();

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                this.soc.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        anArticle.setFullText(fullText.toString());
        System.out.println("DEBUG* Returning full text.");
        return true;
    }

    public String getKeywords(String user) {
        try{
            InetAddress serverAddr = InetAddress.getByName(this.host);
            this.soc = new Socket(serverAddr,this.port);
        }catch(Exception e){
            e.printStackTrace();
            this.soc = null;
            return "";
        }

        StringBuilder keywords = new StringBuilder();
        String request = "@getKeywords;user:" + user + ";";

        try {
            DataOutputStream dout = new DataOutputStream(soc.getOutputStream());
            dout.writeUTF(request);

            BufferedReader br = new BufferedReader(new InputStreamReader(soc.getInputStream()));
            String incoming = "";

            while ((incoming = br.readLine()) != null) {
                //System.out.println("DEBUG* getKeywords incoming: \"" + incoming + "\".");
                if (incoming.replace("\n", "").replace("\r", "").equals("Done")) {
                    break;
                }
                keywords.append(incoming);
            }

            dout.flush();
            dout.close();

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                this.soc.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return keywords.toString();
    }

    public Article getArticle(int index) {
        Article anArticle = this.articles.get(index);
        if (!anArticle.isDownloaded()) {
            downloadArticle(anArticle);
        }
        return anArticle;
    }

    public Article getNextArticle() {
        Article retArt = null;

        if ((this.articles != null) && (this.articleIndex >= 0) && (this.articleIndex < this.articles.size())){
            retArt = this.articles.get(this.articleIndex);
            if (!retArt.isDownloaded()) {
                downloadArticle(retArt);
            }

            if (this.articleIndex <= this.articles.size()) {
                this.articleIndex++;
            }
        }

        return retArt;
    }

    public int countArticles() {
        try{
            return this.articles.size();
        } catch (Exception e){
            return -1;
        }
    }
}
