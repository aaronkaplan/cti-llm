--
-- PostgreSQL database dump
--

-- Dumped from database version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)


--
-- Name: summarydb; Type: DATABASE; Schema: -; Owner: ctillm
--

CREATE DATABASE summarydb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE summarydb OWNER TO ctillm;

\connect summarydb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: score; Type: TABLE; Schema: public; Owner: aaron
--

CREATE TABLE public.score (
    name character varying,
    score numeric,
    fk_summary_id integer,
    reasoning text,
    methodology character varying
);


ALTER TABLE public.score OWNER TO aaron;

--
-- Name: summary; Type: TABLE; Schema: public; Owner: ctillm
--

CREATE TABLE public.summary (
    id integer NOT NULL,
    url text,
    summary text,
    date date,
    human_summary text,
    original_text text,
    sha256_original_text character varying(64),
    llm_response jsonb,
    llm character varying(255)
);


ALTER TABLE public.summary OWNER TO ctillm;

--
-- Name: COLUMN summary.url; Type: COMMENT; Schema: public; Owner: ctillm
--

COMMENT ON COLUMN public.summary.url IS 'The URL of the summarized article';


--
-- Name: COLUMN summary.summary; Type: COMMENT; Schema: public; Owner: ctillm
--

COMMENT ON COLUMN public.summary.summary IS 'The AI generated summary of original_text';


--
-- Name: COLUMN summary.human_summary; Type: COMMENT; Schema: public; Owner: ctillm
--

COMMENT ON COLUMN public.summary.human_summary IS 'If present, a human-written summary so that we can compare the AI summary against it';


--
-- Name: COLUMN summary.llm_response; Type: COMMENT; Schema: public; Owner: ctillm
--

COMMENT ON COLUMN public.summary.llm_response IS 'The (JSON) respone of the LLM. This might contain more than a summary field';


--
-- Name: COLUMN summary.llm; Type: COMMENT; Schema: public; Owner: ctillm
--

COMMENT ON COLUMN public.summary.llm IS 'The model name (string) of the LLM used for the summary';


--
-- Name: summary_id_seq; Type: SEQUENCE; Schema: public; Owner: ctillm
--

CREATE SEQUENCE public.summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.summary_id_seq OWNER TO ctillm;

--
-- Name: summary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ctillm
--

ALTER SEQUENCE public.summary_id_seq OWNED BY public.summary.id;


--
-- Name: summary id; Type: DEFAULT; Schema: public; Owner: ctillm
--

ALTER TABLE ONLY public.summary ALTER COLUMN id SET DEFAULT nextval('public.summary_id_seq'::regclass);


--
-- Name: summary summary_pkey; Type: CONSTRAINT; Schema: public; Owner: ctillm
--

ALTER TABLE ONLY public.summary
    ADD CONSTRAINT summary_pkey PRIMARY KEY (id);


--
-- Name: idx_score_fk_summary_id; Type: INDEX; Schema: public; Owner: aaron
--

CREATE INDEX idx_score_fk_summary_id ON public.score USING btree (fk_summary_id);


--
-- Name: idx_score_name; Type: INDEX; Schema: public; Owner: aaron
--

CREATE INDEX idx_score_name ON public.score USING btree (name);


--
-- Name: idx_summary_llm; Type: INDEX; Schema: public; Owner: ctillm
--

CREATE INDEX idx_summary_llm ON public.summary USING btree (llm);


--
-- Name: idx_summary_sha256; Type: INDEX; Schema: public; Owner: ctillm
--

CREATE INDEX idx_summary_sha256 ON public.summary USING btree (sha256_original_text);


--
-- Name: idx_summary_url; Type: INDEX; Schema: public; Owner: ctillm
--

CREATE INDEX idx_summary_url ON public.summary USING btree (url);


--
-- Name: score score_fk_summary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aaron
--

ALTER TABLE ONLY public.score
    ADD CONSTRAINT score_fk_summary_id_fkey FOREIGN KEY (fk_summary_id) REFERENCES public.summary(id);


--
-- PostgreSQL database dump complete
--

