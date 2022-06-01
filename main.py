import hikari, lightbulb, os

LIGHT_GREEN = hikari.Color.of("#2ecc71")
DARK_GREEN = hikari.Color.of("#1f8b4c")
LIGHT_RED = hikari.Color.of("#e91e63")
DARK_RED = hikari.Color.of("#ad1457")
LIGHT_YELLOW = hikari.Color.of("#f1c40f")
DARK_YELLOW = hikari.Color.of("#c27c0e")

bot = lightbulb.BotApp(token=os.environ["TOKEN"], default_enabled_guilds=[979745570015047820])

@bot.listen(hikari.GuildChannelCreateEvent)
async def setup_mute_on_new_channel(event):
  channel = event.channel
  guild = event.get_guild()
  roles = await guild.fetch_roles()
  muted = None
  for role in roles:
    if role.name == "Muted":
      muted = role
  if not muted:
    muted = await bot.rest.create_role(guild=guild.id, name="Muted", mentionable=False)
  overwrite = hikari.PermissionOverwrite(
    type=hikari.PermissionOverwriteType.ROLE,
    id=muted.id,
    deny=(
      hikari.Permissions.SEND_MESSAGES |
      hikari.Permissions.SEND_MESSAGES_IN_THREADS |
      hikari.Permissions.CREATE_PUBLIC_THREADS |
      hikari.Permissions.CREATE_PRIVATE_THREADS |
      hikari.Permissions.EMBED_LINKS |
      hikari.Permissions.ATTACH_FILES |
      hikari.Permissions.ADD_REACTIONS |
      hikari.Permissions.USE_EXTERNAL_EMOJIS |
      hikari.Permissions.USE_EXTERNAL_STICKERS |
      hikari.Permissions.USE_APPLICATION_COMMANDS
    ),
  )
  overwrites = channel.permission_overwrites[muted.id] = overwrite
  await channel.edit(permission_overwrites=[overwrites])


@bot.listen(hikari.GuildJoinEvent)
async def setup_mute_on_new_guild(event):
  guild = event.get_guild()
  channels = guild.channels
  roles = await guild.fetch_roles()
  muted = None
  for role in roles:
    if role.name == "Muted":
      muted = role
  if not muted:
    muted = await bot.rest.create_role(guild=guild.id, name="Muted", mentionable=False)
  overwrite = hikari.PermissionOverwrite(
    type=hikari.PermissionOverwriteType.ROLE,
    id=muted.id,
    deny=(
      hikari.Permissions.SEND_MESSAGES |
      hikari.Permissions.SEND_MESSAGES_IN_THREADS |
      hikari.Permissions.CREATE_PUBLIC_THREADS |
      hikari.Permissions.CREATE_PRIVATE_THREADS |
      hikari.Permissions.EMBED_LINKS |
      hikari.Permissions.ATTACH_FILES |
      hikari.Permissions.ADD_REACTIONS |
      hikari.Permissions.USE_EXTERNAL_EMOJIS |
      hikari.Permissions.USE_EXTERNAL_STICKERS |
      hikari.Permissions.USE_APPLICATION_COMMANDS
    ),
  )
  for channel in channels:
    overwrites = channel.permission_overwrites[muted.id] = overwrite
    await channel.edit(permission_overwrites=[overwrites])

@bot.command
@lightbulb.option("reason", "Why you muted them", required=False, default="No reason specified", type=str)
@lightbulb.option("member", "Member to mute", required=True, type=hikari.User)
@lightbulb.command("mute", "Kick a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def mute(ctx):
  member = ctx.options.member
  guild = ctx.get_guild()
  reason = ctx.options.reason
  role = ctx.member.get_top_role()
  if role:
    if role.permissions & hikari.Permissions.MANAGE_MESSAGES or ctx.member.id == guild.owner_id:
      muted = None
      for role in await guild.fetch_roles():
        if role.name == "Muted":
          muted = role
      if not muted:
        muted = await bot.rest.create_role(guild=guild.id, name="Muted", mentionable=False)
      try:
        await member.add_role(muted)
      except hikari.errors.ForbiddenError:
        await ctx.respond(embed=hikari.Embed(title=f"❌ Error", description="Hmm It looks like I dont have those permissions it may be because...\n -The Muted Role is above my role\n -I dont have the Manage Roles Permission", color=LIGHT_RED))
      else:
        await ctx.respond(embed=hikari.Embed(title=f"✅ Muted {member}",color=LIGHT_GREEN))  
        await member.send(embed=hikari.Embed(title=f"You were muted from {guild.name}",description=f"You were muted for {reason}",color=LIGHT_YELLOW))
        
    else:
      await ctx.respond(embed=hikari.Embed(title=f"❌ You dont have permissions to manage messages",color=LIGHT_RED))


@bot.command
@lightbulb.option("reason", "Why you kicked them", required=False, default="No reason specified", type=str)
@lightbulb.option("member", "Member to kick", required=True, type=hikari.User)
@lightbulb.command("kick", "Kick a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick(ctx):
  member = ctx.options.member
  reason = ctx.options.reason
  role = ctx.member.get_top_role()
  if role:
    if role.permissions & hikari.Permissions.KICK_MEMBERS or ctx.member.id == ctx.get_guild().owner_id:
      try:
        await member.send(embed=hikari.Embed(title=f"You were kicked from {ctx.get_guild().name}",description=f"You were kicked for {reason}",color=LIGHT_YELLOW))
      except:
        pass
      await ctx.respond(embed=hikari.Embed(title=f"✅ Kicked {member} from the server",color=LIGHT_GREEN))
      await member.kick(reason=reason)
    else:
      await ctx.respond(embed=hikari.Embed(title=f"❌ You dont have permissions to kick members",color=LIGHT_RED))


@bot.command
@lightbulb.option("delete_message_days", "How many days of messages to delete", type=int, required=False, default=0, min_value=0, max_value=7)
@lightbulb.option("reason", "Why you banned them", required=False, default="No reason specified", type=str)
@lightbulb.option("member", "Member to ban", required=True, type=hikari.User)
@lightbulb.command("ban", "Ban a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def ban(ctx):
  member = ctx.options.member  
  reason = ctx.options.reason
  delete_msg_days = ctx.options.delete_message_days
  role = ctx.member.get_top_role()
  if role:
    if role.permissions & hikari.Permissions.BAN_MEMBERS or ctx.member.id == ctx.get_guild().owner_id:
      try:
        await member.send(embed=hikari.Embed(title=f"You were banned from {ctx.get_guild().name}",description=f"You were banned for {reason}",color=LIGHT_RED))
      except:
        pass
      await ctx.respond(embed=hikari.Embed(title=f"✅ Banned {member} from the server",color=LIGHT_GREEN))
      await member.ban(reason=reason, delete_message_days=delete_msg_days)
    else:
      await ctx.respond(embed=hikari.Embed(title=f"❌ You dont have permissions to ban members",color=LIGHT_RED))


bot.run()