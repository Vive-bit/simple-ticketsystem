@bot.command()
async def set_ticket(ctx, *, t=None):
  if ctx.author.id == int(611418916995989534):
    em = discord.Embed(color=discord.Color.blue())
    em.set_author(name="Ticket Erstellen",icon_url=ctx.guild.icon_url)
    em.description = t
    return await ctx.send(embed=em, components=[Button(style=ButtonStyle.blue, label="Ticket Erstellen", custom_id="create_ticket_TAG1")])

TICKET_CHANNELS_ID = 697467411754123285
TICKET_SUPPORTER_ROLE_ID = 712658906727448618
TICKET_LOG_CHANNEL_ID = 715263953093001356

def search_channel(user_id, guild):
  gld = bot.get_guild(guild)
  for ch in gld.channels:
    if ch.category_id != None and int(ch.category_id) == int(TICKET_CHANNELS_ID) and str(ch.type) == "text" and str(ch.topic) == str(user_id):
      return ch.mention
  return False

async def ticket_created_log(cha,user,guild):
  guild = bot.get_guild(int(guild))
  user = guild.get_member(int(user))
  channl = guild.get_channel(int(cha))
  target = guild.get_channel(int(TICKET_LOG_CHANNEL_ID))
  if not channl == None and not user == None and not guild == None:
    em = discord.Embed(color=discord.Color.green())
    em.set_author(name="Ticket Erstellt",icon_url=guild.icon_url)
    em.description = f"Es wurde ein Ticket Erstellt.```\nErsteller: {user} ({user.id})\nChannel: {channl} ({channl.id})```\nZum Ticketchannel: {channl.mention}"
    await target.send(embed=em)
    return
  else:
    print("FATAL ERROR: in ticket_created_log!")
    return


async def create_ticket_m(channel_id, user_id, guild_id):
  guild = bot.get_guild(guild_id)
  cat = guild.get_channel(TICKET_CHANNELS_ID)
  cha = guild.get_channel(channel_id)
  user = guild.get_member(int(user_id))
 # if int(user_id) in datsa["vbanned"]:
 #   return await cha.send("{user.mention}, du bist von den Tickets Gesperrt!",delete_after=7)
  sup_role = get(guild.roles, id=int(TICKET_SUPPORTER_ROLE_ID))
  if not guild == None and not user == None and not cat == None and not sup_role == None and not cha == None:
    try:
      vari = ['vb','gh','ju','rt','as','ui','po','fd','ad','hj','pi','php','js','df']
      varn = random.choice(vari)
      varc = random.randint(10,99)
      channelname = f"{varn}{varc}"
      channl = await guild.create_text_channel(f'🎫- {channelname}',category=cat,topic=user_id)
      await channl.set_permissions(guild.get_role(guild_id), send_messages=False, read_messages=False, read_message_history=False)
      await channl.set_permissions(user, send_messages=True, read_messages=True, add_reactions=False, embed_links=True, attach_files=True, read_message_history=True, external_emojis=False)
      await channl.set_permissions(sup_role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
      await channl.send(f"{sup_role.mention}")
      em = discord.Embed(color=discord.Color.blue())
      em.set_author(name="Ticket Support",icon_url=guild.icon_url)
      em.description = f"Ersteller: {user.mention} ({user.id})\n**Aktionen zur Auswahl:**"
      await channl.send(embed=em, components=[[Button(style=ButtonStyle.blue, label="Ticket Schließen", custom_id="ticket_close"),Button(style=ButtonStyle.red, label="Ticket Löschen", custom_id="ticket_delete")]])
      mh = await channl.send(f":wave: Willkommen im Ticket Support von **{guild.name}**, {user.mention}! Bitte Schildere uns kurz dein Problem bzw. deinen Fall damit wir dir Weiterhelfen können!")
      await mh.pin() 
      try:
        em = discord.Embed(color=discord.Color.blue())
        em.set_author(name="Ticket Erstellt",icon_url=guild.icon_url)
        em.description = f"Dein Ticket auf **{guild.name}** wurde Erfolgreich unter {channl.mention} Erstellt!"
        await user.send(embed=em)
        await cha.send(f"{user.mention}, dein Ticket wurde Erfolgreich Erstellt! Siehe: {channl.mention}",delete_after=5)
        pass
      except:
        await cha.send(f"{user.mention}, dein Ticket wurde Erfolgreich Erstellt! Siehe: {channl.mention}",delete_after=5)
        pass
      await ticket_created_log(channl.id,user.id,guild.id)
      return
    except:
      try:
        await user.send(content=f"{user.mention}, Sorry! Es ist ein Fehler Aufgetreten. Bitte Melde diesen Fehler!")
        pass
      except:
        await cha.send(f"{user.mention}, Sorry! Es ist ein Fehler Aufgetreten. Bitte Melde diesen Fehler!",delete_after=5)
        pass
      return
  else:
    try:
        await user.send(content=f"{user.mention}, Sorry! Es ist ein Fehler Aufgetreten. Bitte Melde diesen Fehler!")
        pass
    except:
        await cha.send(f"{user.mention}, Sorry! Es ist ein Fehler Aufgetreten. Bitte Melde diesen Fehler!",delete_after=5)
        pass
    return
    
def has_suprole(user_id,guild_id):
  role = get(bot.get_guild(guild_id).roles, id=int(TICKET_SUPPORTER_ROLE_ID))
  user = bot.get_guild(guild_id).get_member(int(user_id))
  if not user == None and not role == None:
    if role in user.roles:
      return True
  return False

@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "create_ticket_TAG1":
      u = search_channel(interaction.user.id, interaction.guild.id)
      if u == False:
        await interaction.respond(content=f"{interaction.user.mention} Einen Moment.. Dein Ticket wird Erstellt!")
        return await create_ticket_m(interaction.channel.id, interaction.user.id, interaction.guild.id) 
      else:
        return await interaction.respond(content=f"{interaction.user.mention}, du hast bereits einen Ticket Channel! Schau' mal vorbei: {u}")
    if interaction.custom_id == "ticket_close":
      i = has_suprole(interaction.user.id, interaction.guild.id)
      if i == False:
        return await interaction.respond(content=f"{interaction.user.mention}, du besitzt nicht die benötigten Rechte, um das zu Benutzen!")
      else:
        guild = bot.get_guild(int(interaction.guild.id))
        target = guild.get_channel(int(TICKET_LOG_CHANNEL_ID))
        channj = guild.get_channel(int(interaction.channel.id))
        try:
          user = guild.get_member(int(channj.topic))
          pass
        except:
          user = None
          pass
       # overwritse = channj.overwrites_for(user)
       # if overwritse == None:
        #  return await interaction.respond(content=f"{interaction.user.mention}, dieses Ticket ist bereits Geschlossen!")
        if not user == None:
          em = discord.Embed(color=discord.Color.green())
          em.set_author(name="Ticket Geschlossen",icon_url=guild.icon_url)
          em.description = f"Ersteller: {user.mention} ({user.id})\nGeschlossen von: {interaction.user} ({interaction.user.id})\n**Aktionen zur Auswahl:**"
          await channj.send(embed=em, components=[[Button(style=ButtonStyle.blue, label="Ticket Öffnen", custom_id="ticket_reopen"),Button(style=ButtonStyle.red, label="Ticket Löschen", custom_id="ticket_delete")]])
          await channj.set_permissions(user, overwrite=None)
          if not target == None:
            em = discord.Embed(color=discord.Color.orange())
            em.set_author(name="Ticket Geschlossen",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Geschlossen.```\nErsteller: {user} ({user.id})\nGeschlossen von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
          pass
        else:
          em = discord.Embed(color=discord.Color.green())
          em.set_author(name="Ticket Geschlossen",icon_url=guild.icon_url)
          em.description = f"Ersteller: unkown (Rechte nicht Aktualisiert)\nGeschlossen von: {interaction.user} ({interaction.user.id})\n**Aktionen zur Auswahl:**"
          await channj.send(embed=em, components=[[Button(style=ButtonStyle.blue, label="Ticket Öffnen", custom_id="ticket_reopen"),Button(style=ButtonStyle.red, label="Ticket Löschen", custom_id="ticket_delete")]])
          if not target == None:
            em = discord.Embed(color=discord.Color.orange())
            em.set_author(name="Ticket Geschlossen",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Geschlossen.```\nErsteller: unkown (Rechte nicht Aktualisiert)\nGeschlossen von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
          pass
        await interaction.respond(content="Ticket wird Geschlossen..")
        return
    if interaction.custom_id == "ticket_delete":
      i = has_suprole(interaction.user.id, interaction.guild.id)
      if i == False:
        return await interaction.respond(content=f"{interaction.user.mention}, du besitzt nicht die benötigten Rechte, um das zu Benutzen!")
      else:
        guild = bot.get_guild(int(interaction.guild.id))
        target = guild.get_channel(int(TICKET_LOG_CHANNEL_ID))
        channj = guild.get_channel(int(interaction.channel.id))
        em = discord.Embed(color=discord.Color.orange())
        em.set_author(name="Ticket Delete",icon_url=guild.icon_url)
        em.description = "Einem Moment! Das Ticket wird Gelöscht.."
        await channj.send(embed=em)
        await interaction.respond(content="Ticket wird Gelöscht..")
        await asyncio.sleep(2)
        if not target == None:
          try:
            user = guild.get_member(int(channj.topic))
            pass
          except:
            user = None
            pass
          if not user == None:
            em = discord.Embed(color=discord.Color.red())
            em.set_author(name="Ticket Gelöscht",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Gelöscht.```\nErsteller: {user} ({user.id})\nGelöscht von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
          else:
            em = discord.Embed(color=discord.Color.red())
            em.set_author(name="Ticket Gelöscht",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Gelöscht.```\nErsteller: unkown\nGelöscht von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
        await channj.delete()
        return
    if interaction.custom_id == "ticket_reopen":
      i = has_suprole(interaction.user.id, interaction.guild.id)
      if i == False:
        return await interaction.respond(content=f"{interaction.user.mention}, du besitzt nicht die benötigten Rechte, um das zu Benutzen!")
      else:
        guild = bot.get_guild(int(interaction.guild.id))
        target = guild.get_channel(int(TICKET_LOG_CHANNEL_ID))
        channj = guild.get_channel(int(interaction.channel.id))
        try:
          user = guild.get_member(int(channj.topic))
          pass
        except:
          user = None
          pass
       # overwritse = channj.overwrites_for(user)
       # if overwritse == None:
        #  return await interaction.respond(content=f"{interaction.user.mention}, dieses Ticket ist bereits Geschlossen!")
        if not user == None:
          em = discord.Embed(color=discord.Color.green())
          em.set_author(name="Ticket Geöffnet",icon_url=guild.icon_url)
          em.description = f"Ersteller: {user.mention} ({user.id})\nGeöffnet von: {interaction.user} ({interaction.user.id})\n**Aktionen zur Auswahl:**"
          await channj.send(embed=em, components=[[Button(style=ButtonStyle.blue, label="Ticket Schließen", custom_id="ticket_close"),Button(style=ButtonStyle.red, label="Ticket Löschen", custom_id="ticket_delete")]])
          await channj.set_permissions(user, send_messages=True, read_messages=True, add_reactions=False, embed_links=True, attach_files=True, read_message_history=True, external_emojis=False)
          if not target == None:
            em = discord.Embed(color=discord.Color.green())
            em.set_author(name="Ticket Geöffnet",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Geöffnet.```\nErsteller: {user} ({user.id})\nGeöffnet von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
          pass
        else:
          em = discord.Embed(color=discord.Color.green())
          em.set_author(name="Ticket Geöffnet",icon_url=guild.icon_url)
          em.description = f"Ersteller: unkown (Rechte nicht Aktualisiert)\nGeöffnet von: {interaction.user} ({interaction.user.id})\n**Aktionen zur Auswahl:**"
          await channj.send(embed=em, components=[[Button(style=ButtonStyle.blue, label="Ticket Schließen", custom_id="ticket_close"),Button(style=ButtonStyle.red, label="Ticket Löschen", custom_id="ticket_delete")]])
          if not target == None:
            em = discord.Embed(color=discord.Color.green())
            em.set_author(name="Ticket Geöffnet",icon_url=guild.icon_url)
            em.description = f"Es wurde ein Ticket Geöffnet.```\nErsteller: unkown (Rechte nicht Aktualisiert)\nGeöffnet von: {guild.get_member(int(interaction.user.id))} ({guild.get_member(int(interaction.user.id)).id})\n```\n"
            await target.send(embed=em)
          pass
        await interaction.respond(content="Ticket wird Geöffnet..")
        return
