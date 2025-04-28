package com.esc.wmg.entity;

import java.time.LocalDateTime;

import io.micrometer.common.lang.NonNull;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;

@Entity
@Table(name = "tbl_comment")
@Data
@AllArgsConstructor
@NoArgsConstructor
@RequiredArgsConstructor
public class CommentEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "cmt_idx")
    private long cmt_idx;

    @NonNull
    @Column(name = "post_idx", nullable = false)
    private long postIdx;

    @NonNull
    @Column(name = "cmt_content", nullable = false)
    private String cmt_content;

    @NonNull
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime created_at;

    @NonNull
    @Column(name = "email", nullable = false)
    private String email;

    @Column(name = "parent_idx")
    private Long parent_idx; 



}
