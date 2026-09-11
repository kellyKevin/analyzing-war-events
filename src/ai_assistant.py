"""
AI War Intelligence Assistant for Analyzing War Events.
Provides intelligent analysis, historical Q&A, leader profiles,
fatality statistics, and tactical insights based on conflict datasets.
"""

import pandas as pd
from src.war_data import WAR_METADATA, get_country_metadata

class WarIntelligenceAI:
    def __init__(self, df=None):
        self.df = df

    def set_dataframe(self, df):
        self.df = df

    def ask(self, question: str) -> str:
        """
        Processes user query and returns contextual analysis, historical nostalgia insights,
        country stats, or leader details.
        """
        if not question or not isinstance(question, str):
            return "Please enter a valid question regarding war events or conflict data."

        q = question.lower().strip()

        if self.df is None or self.df.empty:
            return "Intelligence database is empty. Please load dataset first."

        total_events = len(self.df)
        total_fatalities = int(self.df['total_deaths'].sum()) if 'total_deaths' in self.df.columns else 0

        # Check for specific country query
        countries = self.df['country'].dropna().unique() if 'country' in self.df.columns else []
        matched_country = None
        for country in countries:
            if country.lower() in q:
                matched_country = country
                break

        # Check for leaders query
        if "leader" in q or "president" in q or "command" in q or "prime minister" in q:
            if matched_country:
                meta = get_country_metadata(matched_country)
                return (
                    f"⚔️ **Military Leadership Intelligence for {matched_country}**\n\n"
                    f"• **Key Leader / Figure:** {meta['leader']}\n"
                    f"• **Role:** {meta['leader_role']}\n"
                    f"• **Conflict Context:** {meta['era_context']}\n"
                    f"• **Historical Reflective Quote:** *\"{meta['nostalgia_quote']}\"*"
                )
            else:
                leader_list = "\n".join([f"• **{c}**: {data['leader']} ({data['leader_role']})" for c, data in WAR_METADATA.items()])
                return (
                    f"⚔️ **Prominent Conflict Leaders in Active Databases:**\n\n"
                    f"{leader_list}\n\n"
                    f"Ask specifically about any country (e.g., *'Who is the leader of Ukraine in this war?'*) for detailed history."
                )

        # Check for fatalities or deaths query
        if "death" in q or "fatality" in q or "killed" in q or "casualt" in q or "dead" in q:
            if matched_country:
                cdf = self.df[self.df['country'] == matched_country]
                c_deaths = int(cdf['total_deaths'].sum()) if 'total_deaths' in cdf.columns else 0
                c_civ = int(cdf['deaths_civilians'].sum()) if 'deaths_civilians' in cdf.columns else 0
                return (
                    f"📊 **Casualty Breakdown for {matched_country}:**\n\n"
                    f"• Total Reported Fatalities: **{c_deaths}**\n"
                    f"• Civilian Fatalities: **{c_civ}**\n"
                    f"• Total Event Incidents Recorded: **{len(cdf)}**\n\n"
                    f"Remember: Behind every number lies a human story of sacrifice and history."
                )
            else:
                top_countries = self.df.groupby('country')['total_deaths'].sum().sort_values(ascending=False).head(5)
                top_str = "\n".join([f"• **{c}**: {int(d)} fatalities" for c, d in top_countries.items()])
                return (
                    f"🚨 **Global Casualty Intelligence Overview:**\n\n"
                    f"• **Total Recorded Fatalities Across Dataset:** **{total_fatalities}**\n"
                    f"• **Total Conflict Events Analyzed:** **{total_events}**\n\n"
                    f"**Most Impacted Conflict Zones:**\n{top_str}"
                )

        # Check for map / interaction queries
        if "map" in q or "interaction" in q or "location" in q or "hotspot" in q or "where" in q:
            return (
                f"🗺️ **War Interactions & Spatial Map Intelligence:**\n\n"
                f"The interactive tactical map renders all **{total_events}** georeferenced war event points globally. "
                f"Circle markers reflect fatality volume (yellow for minor, orange for moderate, red for heavy casualties). "
                f"Clicking on any hotspot reveals country flags, side A vs side B fatalities, civilian casualties, and historical leader profiles."
            )

        # Check for specific country general query
        if matched_country:
            cdf = self.df[self.df['country'] == matched_country]
            c_deaths = int(cdf['total_deaths'].sum()) if 'total_deaths' in cdf.columns else 0
            meta = get_country_metadata(matched_country)
            years = sorted(cdf['year'].unique()) if 'year' in cdf.columns else []
            years_str = ", ".join(map(str, years))
            return (
                f"🌍 **War Intelligence Report: {matched_country}**\n\n"
                f"• **Active Years:** {years_str}\n"
                f"• **Recorded Conflict Events:** {len(cdf)}\n"
                f"• **Total Fatalities:** {c_deaths}\n"
                f"• **Primary Leader / Commander:** {meta['leader']} ({meta['leader_role']})\n"
                f"• **Historical Context:** {meta['era_context']}\n"
                f"• **Historical Reflective Quote:** *\"{meta['nostalgia_quote']}\"*\n"
            )

        # Check for trend / year query
        if "trend" in q or "year" in q or "time" in q or "history" in q or "most" in q:
            if 'year' in self.df.columns and 'total_deaths' in self.df.columns:
                yearly = self.df.groupby('year')['total_deaths'].sum()
                peak_year = yearly.idxmax()
                peak_deaths = int(yearly.max())
                return (
                    f"📈 **Historical Temporal Trends Analysis:**\n\n"
                    f"• Highest conflict severity occurred in year **{peak_year}** with **{peak_deaths}** total fatalities.\n"
                    f"• Total timeline spans from **{self.df['year'].min()}** to **{self.df['year'].max()}**.\n"
                    f"War history shows how intense conflict cycles fluctuate across time and geography."
                )

        # Default nostalgic war AI response with dynamic summary
        return (
            f"🪖 **War Intelligence AI Assistant:**\n\n"
            f"I have analyzed **{total_events}** conflict incidents totaling **{total_fatalities}** recorded casualties across **{len(countries)}** nations.\n\n"
            f"You can ask me questions such as:\n"
            f"1. *'Who is the leader of Ukraine or Syria in this war?'*\n"
            f"2. *'What are the total casualties in Sudan?'*\n"
            f"3. *'Which year had the highest fatalities?'*\n"
            f"4. *'Explain the map war interactions'* or *'Show leader profile for Ethiopia'*"
        )
