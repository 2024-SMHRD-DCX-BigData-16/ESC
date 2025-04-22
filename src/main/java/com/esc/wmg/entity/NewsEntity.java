package com.esc.wmg.entity;

import java.time.LocalDateTime;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Entity
@Table(name = "tbl_news")
@Data
@AllArgsConstructor
@NoArgsConstructor
@RequiredArgsConstructor
public class NewsEntity {
    //채팅 하나의 번호
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long chat_idx;

    @NonNull
    @Column(name = "news_idx", nullable = false)
    /**
     * news_idx 는 뉴스의 고유 번호를 저장하는 컬럼
     */
    private String news_idx;

    @NonNull
    @Column(name = "news_title", nullable = false)
    private String news_title;

    @NonNull
    @Column(name = "news_writer", nullable = false)
    /**
     * news_writer 뉴스의 언론사 
     */
    private String news_writer;


    @Column(name = "news_img")
    /**
     * news_img 뉴스의 썸내일 이미지
     */
    private String news_img;


    @Column(name = "date")
    @CreationTimestamp
    /**
     * date는 뉴스의 작성일자
     */
    private String date;


    @Column(name = "crawled_at")
    @UpdateTimestamp
    /**
     * crawled_at는 뉴스의 크롤링 + 분류 일자
     */
    private String crawled_at;



}
