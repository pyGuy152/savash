
import { useEffect, useState } from "react";

import { apiUrl, getToken, LOGOUT, post} from "../types.ts";

import "./Posts.css";

interface PostsProps{
    classID : Number
}

function Posts({ classID } : PostsProps){

    const [posts, setPosts] = useState<any[]>([]);

    useEffect(() => {
        fetch(apiUrl + "/classes/" + classID + "/posts/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "bearer " + getToken(document.cookie)
            }
        })
        .then((res) => {
            if(res.status === 401){
                window.location.href = "/login";
            }
            return res.json();
        })
        .then((data) => {
            console.log(data);
            let parsedData = data.map((post: post) => {
                return {
                    ...post,
                    posted_at: new Date(post.posted_at)
                }
            });
            console.log(parsedData);
            setPosts(parsedData);
        })
        .catch(() => {
            LOGOUT();
        })
    }, [])
    return (
      <div>
        <div className="posts">
          {posts.length === 0 ? (
            <p>No posts available.</p>
          ) : (
            posts.map((post) => (
              <div key={post.post_id} className="post">
                <div>
                  <h3>{post.title}</h3>
                  <p>{post.content}</p>
                </div>
                <div className="row">
                  <p className="post-meta">{post.user_name}</p>
                  <p className="post-meta">-</p>
                  <p className="post-meta">
                    {post.posted_at.toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    );
}

export default Posts;